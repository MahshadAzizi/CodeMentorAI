from fastapi import FastAPI
from code_analysis_service.app.routers.analysis import router as analyze_router

app = FastAPI(
    title="Code Analysis Service",
    description="Handles repo download and function analysis"
)

api_prefix = '/api/v1'

app.include_router(analyze_router, prefix=f'{api_prefix}/analyze', tags=['analyze'])
