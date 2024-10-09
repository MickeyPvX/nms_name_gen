"""Azure Properties models"""

from pydantic import BaseModel, HttpUrl


class AzureProperties(BaseModel):
    """Data model for Azure translator properties"""

    translate_url: HttpUrl
    translate_key: str
