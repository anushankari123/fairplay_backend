import bcrypt
from uuid import UUID
from sqlmodel import col
from api.db.models.user import User
from api.interfaces.utils import List
from api.interfaces.user import UserRead, UserCreate, UserUpdate, UserLogin
from api.utils.exceptions import NotFoundError, DuplicateConstraint, AuthenticationError
from .base import BaseService
import jwt
import os
from datetime import datetime, timedelta


class UserService(BaseService):
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def _create_access_token(self, user_id: UUID) -> str:
        """
        Create a JWT access token
        """
        secret_key = os.getenv('JWT_SECRET_KEY', 'your_very_secret_key')
        payload = {
            'sub': str(user_id),
            'exp': datetime.utcnow() + timedelta(hours=2)
        }
        return jwt.encode(payload, secret_key, algorithm='HS256')

    async def login(self, login_data: UserLogin):
        """
        Authenticate a user and return an access token
        """
        res = await User.get(db=self.db, filters=[User.email == login_data.email, ~col(User.is_deleted)])
        user = res.one_or_none()

        if not user or not self._verify_password(login_data.password, user.password):
            raise AuthenticationError("Invalid email or password")

        access_token = self._create_access_token(user.id)
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number
        }
    
    async def get_user(self, user_id: UUID) -> UserRead:
        """
        Retrieve a specific user by their UUID.

        Args:
        - user_id (UUID): The UUID of the user to retrieve.

        Returns:
        - UserRead: Details of the retrieved user.

        Raises:
        - NotFoundError: Raised if the user is not found.
        """
        # pylint: disable=invalid-unary-operand-type
        res = await User.get(db=self.db, filters=[User.id == user_id, ~col(User.is_deleted)])
        user = res.one_or_none()
        if user is None:
            raise NotFoundError("User not found")
        return user

    async def get_users(self) -> List[UserRead]:
        """
        Retrieve a list of non-deleted users.

        Returns:
        - List[UserRead]: List of non-deleted users.
        """
        # pylint: disable=invalid-unary-operand-type
        res = await User.get(db=self.db, filters=[~col(User.is_deleted)])
        return {"data": res.all()}

    async def get_internal_users(self) -> List[UserRead]:
        """
        Retrieve a list of internal users, including those marked as deleted.

        Returns:
        - List[UserRead]: List of internal users.
        """
        res = await User.get(db=self.db)
        return {"data": res.all()}

    async def validate_unique_user(self, email: str = None, user_id: UUID = None):
        """
        Validate that the given email is unique.

        Args:
        - email (str): Email to check for uniqueness.
        - user_id (UUID): User ID to exclude from the uniqueness check.

        Raises:
        - DuplicateConstraint: Raised if a user with the same email already exists.
        """
        # Check for unique email
        if email:
            existing_user = await User.get(db=self.db, filters=[User.email == email])
            if (user := existing_user.one_or_none()) and user.id != user_id:
                raise DuplicateConstraint("Email is already taken")

    async def create_user(self, data: UserCreate) -> UserRead:
        """
        Create a new user.

        Args:
        - data (UserCreate): Information to create the user.

        Returns:
        - UserRead: Details of the created user.

        Raises:
        - DuplicateConstraint: Raised if a user with the same email already exists.
        """
        await self.validate_unique_user(email=data.email)

        data.password = self._hash_password(data.password)

        new_user = User(**data.model_dump())
        await new_user.save(self.db)
        return new_user

    async def delete_user(self, user_id: UUID):
        """
        Mark a user as deleted.

        Args:
        - user_id (UUID): The UUID of the user to delete.
        """
        user = await self.get_user(user_id)
        user.is_deleted = True
        await user.save(self.db)

    async def update_user(self, user_id: UUID, data: UserUpdate) -> UserRead:
        """
        Update details of a user.

        Args:
        - user_id (UUID): The UUID of the user to update.
        - data (UserUpdate): Information to update the user.

        Returns:
        - UserRead: Details of the updated user.

        Raises:
        - DuplicateConstraint: Raised if a user with the same email already exists.
        """
        await self.validate_unique_user(
            email=getattr(data, "email", None), user_id=user_id
        )

        user = await self.get_user(user_id)
        await user.update(self.db, data)
        return user
