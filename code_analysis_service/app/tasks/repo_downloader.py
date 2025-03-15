import logging
import os
from git import Repo
from code_analysis_service.app.models import Job, JobStatus
from code_analysis_service.app.config.db import SessionLocal
from code_analysis_service.app.config.celery import celery_app

logger = logging.getLogger(__name__)


DOWNLOAD_FOLDER = "./repos"


@celery_app.task(name="code_analysis_service.app.tasks.repo_downloader.download_repo")
def download_repo(job_id: str, repo_url: str):
    db = SessionLocal()
    try:
        logger.info(f"[Celery] Starting job {job_id}")

        job = db.query(Job).filter(Job.uuid == job_id).first()
        if not job:
            logger.error(f"Job {job_id} not found in DB")
            return

        job.status = JobStatus.DOWNLOADING
        db.commit()

        repo_folder = os.path.join(DOWNLOAD_FOLDER, job_id)
        os.makedirs(repo_folder, exist_ok=True)

        Repo.clone_from(repo_url, repo_folder)

        job.status = JobStatus.DONE
        job.local_path = repo_folder
        db.commit()

        logging.info(f"[Celery] Repo downloaded successfully for job {job_id}")

    except Exception as e:
        logger.error(f"[Celery] Failed to download repo for job {job_id}: {e}")
        job.status = JobStatus.FAILED
        db.commit()

    finally:
        db.close()
