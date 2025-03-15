from uuid import UUID

from pydantic import BaseModel


class StartAnalyzeSchema(BaseModel):
    repo_url: str


class StartAnalyzeOutputSchema(BaseModel):
    job_id: UUID

