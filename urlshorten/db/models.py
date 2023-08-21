# type: ignore
from sqlalchemy import BOOLEAN, Column, String

from urlshorten.db.base_model import BaseModel


class DBShortenedUrl(BaseModel):
    __tablename__ = "shortened_urls"

    destination_url = Column(String, nullable=False)
    enabled = Column(BOOLEAN, nullable=False, default=True)
