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


@router.post("/function", response_model=AnalyzeFunctionResponse)
async def function_analysis(
        db: Session = Depends(get_db),
        request: AnalyzeFunctionRequest = Body(...)
):
    job_selector = JobByUUIDRetrieval(db)
    job = job_selector.get_job_by_uuid(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != JobStatus.DONE:
        raise HTTPException(status_code=400, detail="Job is not ready. Status: " + job.status.value)
    repo_path = job.local_path
    function_code = extract_function_code(repo_path, request.function_name)
    logger.info(function_code)
    return AnalyzeFunctionResponse(suggestions=['suggestions'])
