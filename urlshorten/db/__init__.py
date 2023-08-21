from .base import Base
from .session import SessionLocal

# NOTE: This line can't be removed as alembic use it for migration control
from urlshorten.db.models import *  # isort:skip
