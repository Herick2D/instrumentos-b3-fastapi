 
import pandas as pd
from celery import Celery
from pymongo import MongoClient
from config import get_settings
import io

settings = get_settings()

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URI,
    backend=settings.REDIS_URI
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task
def process_file_task(file_content_bytes: bytes, filename: str, content_type: str):
    client = MongoClient(settings.MONGO_URI)
    db = client.file_database

    try:
        if content_type == 'text/csv':
            df = pd.read_csv(io.BytesIO(file_content_bytes))
        elif content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(file_content_bytes))
        else:
            db.upload_history.update_one(
                {"filename": filename},
                {"$set": {"status": "failed", "error": "Unsupported file type"}}
            )
            return

        records = df.to_dict('records')
        db.file_content.insert_many(records)

        db.upload_history.update_one(
            {"filename": filename},
            {"$set": {"status": "completed", "record_count": len(records)}}
        )
    except Exception as e:
        db.upload_history.update_one(
            {"filename": filename},
            {"$set": {"status": "failed", "error": str(e)}}
        )
    finally:
        client.close()