from uuid import UUID

from pydantic import BaseModel


class JobSchema(BaseModel):
    uuid: UUID
    repo_url: str
    local_path: str
    status: str

    class Config:
        from_attributes = True

