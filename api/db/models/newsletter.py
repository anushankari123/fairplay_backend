from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class Newsletter(SQLModel, table=True):
    __tablename__ = "newsletter_subscriptions"

    # Set email as the primary key
    email: EmailStr = Field(..., description="Email address of the subscriber", primary_key=True, nullable=False, index=True, unique=True)
