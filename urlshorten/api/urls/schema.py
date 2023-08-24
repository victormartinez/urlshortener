from typing import Optional

from pydantic import BaseModel, Field


class DestinationUrlIn(BaseModel):
    destination_url: str = Field(
        ...,
        title="URL",
        description="Specifies the url that will be shortened.",
        example="https://google.com",
    )


class DestinationUrlOut(BaseModel):
    destination_url: str = Field(
        ...,
        title="URL",
        description="Specifies the url.",
        example="https://google.com",
    )


class CodeUrlOut(BaseModel):
    code: str = Field(
        ...,
        title="Shortened Url Code",
        description="Specifies the code that represents the shortened URL.",
        example="a8Nsl9ZL",
    )


class UpdateDestinationUrlIn(BaseModel):
    destination_url: Optional[str] = Field(
        title="URL",
        description="Specifies the new url related to the code.",
        example="https://bing.com",
    )
    enabled: Optional[bool] = Field(
        title="Enabled",
        description="Specifies whether the url will be available to be redirected to.",
        example=True,
    )
