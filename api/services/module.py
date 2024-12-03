from uuid import UUID
from api.db.models.module import Module
from api.interfaces.utils import List
from api.interfaces.module import ModuleRead, ModuleCreate, ModuleUpdate
from api.utils.exceptions import NotFoundError
from .base import BaseService


class ModuleService(BaseService):
    async def get_module(self, module_id: UUID) -> ModuleRead:
        res = await Module.get(self.db, filters=[Module.id == module_id])
        module = res.one_or_none()
        if not module:
            raise NotFoundError("Module not found")
        return module

    async def create_module(self, data: ModuleCreate) -> ModuleRead:
        new_module = Module(**data.model_dump())
        await new_module.save(self.db)
        return new_module

    async def delete_module(self, module_id: UUID):
        module = await self.get_module(module_id)
        module.is_deleted = True
        await module.save(self.db)

    async def get_modules(self) -> List[ModuleRead]:
        """
        Retrieve a list of non-deleted modules.

        Returns:
        - List[ModuleRead]: List of non-deleted modules.
        """
        res = await Module.get(self.db, filters=[~Module.is_deleted])  # Fetch modules where is_deleted is False
        return {"data": res.all()}
    
    async def set_quiz_score(self, user_id: UUID, module_id: UUID, quiz_score: int) -> ModuleRead:
        module = await self.get_module(module_id)
        if module.user_id != user_id:
            raise NotFoundError("Module does not belong to this user")
        module.quiz_score = quiz_score
        await module.save(self.db)
        return module

    # New method to get the quiz score for a user and module
    async def get_quiz_score_for_user(self, module_id: UUID, user_id: UUID) -> Module:
        # Query to fetch the module for the given module_id and user_id, ensuring it is not deleted
        res = await Module.get(self.db, filters=[Module.user_id == user_id, Module.id == module_id, ~Module.is_deleted])
        module = res.one_or_none()  # Get the first matching result or None

        if not module:
            raise NotFoundError(f"Module with ID {module_id} for user with ID {user_id} not found")

        return module

    # New method to increment modules in progress and completed
    async def increment_module_progress(self, user_id: UUID, increment_completed: bool = False, increment_in_progress: bool = False) -> Module:
        # Query to fetch the module for the given user_id, ensuring it is not deleted
        res = await Module.get(self.db, filters=[Module.user_id == user_id, ~Module.is_deleted])
        module = res.one_or_none()  # Get the first matching result or None

        if not module:
            raise NotFoundError("Module not found for this user")

        # Increment the respective fields if specified
        if increment_completed:
            module.modules_completed += 1

        if increment_in_progress:
            module.modules_in_progress += 1
        
        # Save the updated module back to the database
        await module.save(self.db)
        
        return module
    
