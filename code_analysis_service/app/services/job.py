import logging
import uuid

from sqlalchemy.orm import Session

from code_analysis_service.app.models import Job

logger = logging.getLogger(__name__)


class JobService:
    def __init__(self, repo_url, db: Session):
        self.repo_url = repo_url
        self.db = db

    def create_job(self):
        job = Job(
            uuid=str(uuid.uuid4()),
            repo_url=self.repo_url,
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
