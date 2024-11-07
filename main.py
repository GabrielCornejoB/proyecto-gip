from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from application.DataUploadController import DataUploadController
from application.ModelPredictionController import ModelPredictionController
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(DataUploadController)
app.include_router(ModelPredictionController)

