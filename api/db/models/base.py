from typing import Any, Type, TypeVar, Optional, Callable
from uuid import UUID
from datetime import datetime
from uuid_extensions import uuid7
from pydantic import field_serializer
from sqlmodel import Session, SQLModel, Field, select
from sqlmodel.sql.expression import SelectOfScalar
from api.interfaces.utils import QueryFilterType

T = TypeVar("T", bound=SQLModel)

# Define operator map: Mapping of operators to corresponding SQLAlchemy expressions.
__operator_map: dict[str, Callable] = {
    "==": lambda column, value: column == value,
    "!=": lambda column, value: column != value,
    "not": lambda column, _: ~column,  # NOT operation
    ">": lambda column, value: column > value,
    "<": lambda column, value: column < value,
    ">=": lambda column, value: column >= value,
    "<=": lambda column, value: column <= value,
    "in": lambda column, value: column.in_(value),
    "not in": lambda column, value: column.notin_(value),
    "like": lambda column, value: column.like(value),
}


class BaseModel(SQLModel):

    @classmethod
    async def get(cls: Type[T], db: Session, columns: Optional[list] = None, filters: Optional[QueryFilterType] = None):
        """
        This is a class method helps to generate an SQL Query and returns the resultant after execution of the query

        Args:
        db: instance of Session from SQLModel to run query
        columns (optional): List of columns or models whose data to be fetched in the query.
                        Columns should be in form of SQLAlchemy. eg: [Users.id, Users.email]
        filters (optional): List or dictionary of conditions to be added on to the `where` clause of the query
                        Filters can either be in the form of list or dictionary.
                            - If list, each item should be a SQLAlchemy condition.
                                Examples: [User.id == "123124", User.email == "abc@def.com"]
                                [User.age < 30, User.name.like("J%")]

                            - If dictionary, it should be in the form of {column: {"operator": "operator", "value": value}}.
                                Examples: {User.name: {"operator": "==", "value": "Alice"}}
                                          {User.is_deleted: {"operator": "not", "value": None}} - Query users where is_deleted is false
                                          {User.name: {"operator": "like", "value": "J%"}}

                            Supported operators include:
                                - "==": Equality
                                - "!=": Inequality
                                - "not": Not operation (~)
                                - ">": Greater than
                                - "<": Less than
                                - ">=": Greater than or equal to
                                - "<=": Less than or equal to
                                - "in": Inclusion in a list
                                - "not in": Exclusion from a list
                                - "like": Pattern matching (LIKE in SQL)

        Returns:
            List[T]: A list of instances of the model class matching the query criteria.

        There is a wide scope of improvement here.
        - The filters need to be a proper condition. It cannot auto setup the conditions for `where` clause
        - TODO: It needs to have feature to support join and accept necessary join conditions (for now it can be done with filters too)
        """
        query: SelectOfScalar = select(cls) if columns is None else select(*columns)
        if isinstance(filters, dict):
            filters = [__operator_map[info["operator"]](col, info.get("value", None)) for col, info in filters.items()]
        if filters:
            query: SelectOfScalar = query.where(*filters)
        return await db.exec(query)

    @classmethod
    async def get_multi(cls: Type[T], db: Session, skip: int = 0, limit: int = 10) -> list[T]:
        result = await db.execute(select(cls).offset(skip).limit(limit))
        return result.all()

    @classmethod
    async def all(cls: Type[T], db: Session):
        return await db.exec(select(cls)).all()

    async def save(self, db: Session):
        db.add(self)
        await db.flush()
        await db.refresh(self)

    async def update(self, db: Session, source: dict | SQLModel):
        if isinstance(source, SQLModel):
            source = source.dict(exclude_unset=True)

        for key, value in source.items():
            setattr(self, key, value)
        await self.save(db)

    async def delete(self, db: Session, hard_delete: bool = False):
        if hard_delete:
            await db.delete(self)
            await db.flush()
        else:
            await self.update(
                db,
                {
                    "is_deleted": True,
                    "deleted_at": datetime.now(),
                },
            )

    async def restore(self, db: Session):
        await self.update(
            db,
            {
                "is_deleted": False,
                "deleted_at": None,
            },
        )


class IdMixin(SQLModel):
    """
    'IdMixin' SQLModel base class for the `id` field

    - 'id': Unique identifier (UUID) for the record
    """

    id: UUID = Field(
        description="Unique ID field - UUID",
        # prefer uuid v7 as id
        # https://datatracker.ietf.org/doc/html/draft-peabody-dispatch-new-uuid-format#section-5.2
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimestampMixin(SQLModel):
    """
    'TimestampMixin' SQLModel base class for the fields - `created_at`, `updated_at`

    - 'created_at': Timestamp for the creation of the record.
    - 'updated_at': Timestamp for the last update of the record.

    Adds 'created_at' and 'updated_at' fields with default values for the creation timestamp and update timestamp.
    """

    created_at: datetime = Field(
        description="Creation time",
        default_factory=datetime.now,
        nullable=False,
    )
    updated_at: datetime = Field(
        description="Update time",
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )

    @field_serializer("created_at")
    def serialize_dt(self, created_at: datetime | None, _info: Any) -> str | None:
        if created_at is not None:
            return created_at.isoformat()
        return None

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime | None, _info: Any) -> str | None:
        if updated_at is not None:
            return updated_at.isoformat()

        return None


class SoftDeleteMixin(SQLModel):
    """
    'SoftDeleteMixin' SQLModel base class for the field - `is_deleted`
    to handle soft delete of the record

    - 'deleted_at': Timestamp for the deletion of the record (soft deletion).
    - 'is_deleted': Flag indicating whether the record is deleted (soft deletion).

    Adds 'deleted_at' and 'is_deleted' fields for soft deletion functionality.
    """

    is_deleted: bool = Field(
        default=False,
        # every select query will check for softdeletion, so index is needed
        index=True,
        description="Flag indicating whether the record is deleted (soft deletion)",
    )
    deleted_at: datetime | None = Field(
        default=None,
        description="Timestamp for the deletion of the record (soft deletion)",
    )

    @field_serializer("deleted_at")
    def serialize_dates(self, deleted_at: datetime | None, _info: Any) -> str | None:
        if deleted_at is not None:
            return deleted_at.isoformat()

        return None
