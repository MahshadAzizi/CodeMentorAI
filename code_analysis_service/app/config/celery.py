from celery import Celery

from code_analysis_service.app.config.settings import settings

celery_app = Celery(
    "code_analysis_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.autodiscover_tasks(['code_analysis_service.app.tasks'])

celery_app.conf.task_routes = {
    "code_analysis_service.app.tasks.repo_downloader.*": {"queue": "code_analysis_queue"},
}
