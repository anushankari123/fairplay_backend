from uuid import UUID
from sqlmodel import col
from api.db.models.user import User
from api.interfaces.utils import List
from api.interfaces.user import UserRead, UserCreate, UserUpdate
from api.utils.exceptions import NotFoundError, DuplicateConstraint
from .base import BaseService


class UserService(BaseService):
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

    async def validate_unique_user(self, email: str = None, phone_number: str = None, user_id: UUID = None):
        """
        Validate that the given email and phone number are unique.

        Args:
        - email (str): Email to check for uniqueness.
        - phone_number (str): Phone number to check for uniqueness.
        - user_id (UUID): User ID to exclude from the uniqueness check.

        Raises:
        - DuplicateConstraint: Raised if a user with the same email or phone number already exists.
        """
        # Check for unique email
        if email:
            existing_user = await User.get(db=self.db, filters=[User.email == email])
            if (user := existing_user.one_or_none()) and user.id != user_id:
                raise DuplicateConstraint("Email is already taken")

        # Check for unique phone number
        if phone_number:
            existing_user = await User.get(db=self.db, filters=[User.phone_number == phone_number])
            if (user := existing_user.one_or_none()) and user.id != user_id:
                raise DuplicateConstraint("Phone number is already taken")

    async def create_user(self, data: UserCreate) -> UserRead:
        """
        Create a new user.

        Args:
        - data (UserCreate): Information to create the user.

        Returns:
        - UserRead: Details of the created user.

        Raises:
        - DuplicateConstraint: Raised if a user with the same email or phone number already exists.
        """
        await self.validate_unique_user(email=data.email, phone_number=data.phone_number)

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
        - DuplicateConstraint: Raised if a user with the same email or phone number already exists.
        """
        await self.validate_unique_user(
            email=getattr(data, "email", None), phone_number=getattr(data, "phone_number", None), user_id=user_id
        )

        user = await self.get_user(user_id)
        await user.update(self.db, data)
        return user
