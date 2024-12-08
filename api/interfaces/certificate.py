from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, HttpUrl

class CertificateCreate(BaseModel):
    module_quiz_id: UUID
    user_id: UUID
    module_name: Optional[str] = None
    score: Optional[int] = None
    certificate_url: Optional[str] = None

    model_config = ConfigDict(extra='forbid')

class CertificateRead(BaseModel):
    id: UUID
    module_quiz_id: UUID
    user_id: UUID
    module_name: str
    score: int
    certificate_url: Optional[str] = None

class CertificateUpdate(BaseModel):
    module_name: Optional[str] = None
    score: Optional[int] = None
    certificate_url: Optional[str] = None

    model_config = ConfigDict(extra='forbid')