import logging

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from code_analysis_service.app.config.db import get_db
from code_analysis_service.app.models import JobStatus
from code_analysis_service.app.queries.retrieve_job_by_uuid import JobByUUIDRetrieval
from code_analysis_service.app.schema import StartAnalyzeSchema, StartAnalyzeOutputSchema, AnalyzeFunctionResponse, \
    AnalyzeFunctionRequest
from code_analysis_service.app.services.function_extractor import extract_function_code
from code_analysis_service.app.services.job import JobService
from code_analysis_service.app.tasks.repo_downloader import download_repo

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/start", response_model=StartAnalyzeOutputSchema)
async def start_analysis(
        db: Session = Depends(get_db),
        request: StartAnalyzeSchema = Body(...)
):
    job_service = JobService(request.repo_url, db)
    job = job_service.create_job()
    download_repo.delay(str(job.uuid), job.repo_url)
    return StartAnalyzeOutputSchema(job_id=job.uuid)



