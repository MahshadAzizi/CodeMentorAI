import logging

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from code_analysis_service.app.config.db import get_db
from code_analysis_service.app.schema import StartAnalyzeSchema, StartAnalyzeOutputSchema
from code_analysis_service.app.services.job import JobService
from code_analysis_service.app.tasks.repo_downloader import download_repo


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/start", response_model=StartAnalyzeOutputSchema)
async def start_analysis(
        db: Session = Depends(get_db),
        repo_url: StartAnalyzeSchema = Body(...)
):
    logger.info('router')
    logger.info(repo_url)
    job_service = JobService(repo_url.repo_url, db)
    job = job_service.create_job()
    logger.info(job.uuid)
    logger.info(job.repo_url)
    download_repo.delay(str(job.uuid), job.repo_url)
    return {"job_id": job.uuid}
