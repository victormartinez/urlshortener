# type: ignore
from sqlalchemy import BOOLEAN, VARCHAR, Column, String

from urlshorten.db.base_model import BaseModel


class DBShortenedUrl(BaseModel):
    __tablename__ = "shortened_urls"

    code = Column(VARCHAR, nullable=False, unique=True, index=True)
    destination_url = Column(String, nullable=False)
    enabled = Column(BOOLEAN, nullable=False, default=True)
