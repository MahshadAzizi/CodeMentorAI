from sqlalchemy.orm import Session
from code_analysis_service.app.models import Job


class JobByUUIDRetrieval:
    def __init__(self, db: Session):
        self.db = db

    def get_job_by_uuid(self, uuid: str):

        job = self.db.query(Job).filter(Job.uuid == uuid).first()
        if not job:
            return None
        return job
