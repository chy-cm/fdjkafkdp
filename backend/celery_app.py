from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "cinesynopsis",
    broker=redis_url,
    backend=redis_url,
    include=["tasks.video_task"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
