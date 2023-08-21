from pydantic import BaseModel


class ShortenedUrl(BaseModel):
    code: str
    destination_url: str
    enabled: bool
