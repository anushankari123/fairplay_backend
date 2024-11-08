from typing import Generic, TypeVar, Union, TypeAlias, Any
from pydantic import BaseModel
from sqlmodel.sql.expression import BinaryExpression

# Generic type variable for the schema used in the list response
T = TypeVar("T", bound=BaseModel)


# Generic BaseModel for a list response
class List(BaseModel, Generic[T]):
    """
    Description:
    ----------
    Schema for representing a list response.

    Fields:
    ----------
    - 'data' (List[SchemaType]): List of items in the response.
    """

    data: list[T]


# Define a type alias for filters passed to get method of BaseModel.Filters can be a list of binary expressions or a dictionary
# - TODO: In dict[str,Any] structure must be more specific instead of using Any.
QueryFilterType: TypeAlias = Union[list[BinaryExpression], dict[str, Any]]
