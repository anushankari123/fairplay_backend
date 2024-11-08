# docker run --name redin_ecomm -e POSTGRES_PASSWORD=admin -e POSTGRES_USER=redin_admin -e POSTGRES_DB=redin_DB  -d -p 5432:5432 postgres
from .base import IdMixin, TimestampMixin, SoftDeleteMixin
