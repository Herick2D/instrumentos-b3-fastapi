from celery import Celery
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import get_settings
import io
import csv

settings = get_settings()
celery_app = Celery("tasks", broker=settings.REDIS_URI, backend=settings.REDIS_URI)


@celery_app.task
def process_file_task(upload_id: str, file_content_bytes: bytes, content_type: str):
    client = MongoClient(settings.MONGO_URI)
    db = client.file_database
    history_collection = db.upload_history
    content_collection = db.file_content

    upload_oid = ObjectId(upload_id)

    history_collection.update_one({"_id": upload_oid}, {"$set": {"status": "processing"}})

    try:
        data_to_insert = []
        total_rows = 0
        chunk_size = 1000

        file_like_object = io.StringIO(file_content_bytes.decode('latin1'))

        next(file_like_object, None)
        next(file_like_object, None)

        reader = csv.reader(file_like_object, delimiter=';')

        for row in reader:
            if not row or row[0] == 'TRAILER' or not row[1]:
                continue

            def get_from_row(r, index, default=None):
                try:
                    return r[index] if r[index] else default
                except IndexError:
                    return default

            instrument_data = {
                'upload_id': upload_id,
                'RptDt': get_from_row(row, 0),
                'TckrSymb': get_from_row(row, 1),
                'MktNm': get_from_row(row, 5),
                'SctyCtgyNm': get_from_row(row, 6),
                'ISIN': get_from_row(row, 16),
                'CrpnNm': get_from_row(row, 49),
            }
            data_to_insert.append(instrument_data)

            if len(data_to_insert) >= chunk_size:
                content_collection.insert_many(data_to_insert)
                total_rows += len(data_to_insert)
                data_to_insert = []

        if data_to_insert:
            content_collection.insert_many(data_to_insert)
            total_rows += len(data_to_insert)

        history_collection.update_one(
            {"_id": upload_oid},
            {"$set": {"status": "completed", "record_count": total_rows}}
        )

    except Exception as e:
        history_collection.update_one(
            {"_id": upload_oid},
            {"$set": {"status": "failed", "error": str(e)}}
        )
    finally:
        client.close()