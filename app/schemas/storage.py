from pydantic import BaseModel

class FileUploadedScheme(BaseModel):
  url: str