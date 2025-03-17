from typing import List
from uuid import UUID

from pydantic import BaseModel


class StartAnalyzeSchema(BaseModel):
    repo_url: str


class StartAnalyzeOutputSchema(BaseModel):
    job_id: UUID


class AnalyzeFunctionRequest(BaseModel):
    job_id: str
    function_name: str


class AnalyzeFunctionResponse(BaseModel):
    suggestions: List[str]
