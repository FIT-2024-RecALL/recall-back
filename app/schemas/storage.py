from pydantic import BaseModel

__all__ = ["FileUploadedScheme"]


class FileUploadedScheme(BaseModel):
    url: str
