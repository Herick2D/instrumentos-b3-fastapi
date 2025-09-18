from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, status
from pymongo import MongoClient
from datetime import datetime
import hashlib

from config import get_settings
from tasks import process_file_task
from auth import get_api_key

router = APIRouter()
settings = get_settings()

@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(
        file: UploadFile = File(...),
        api_key: str = Depends(get_api_key)
):
    file_content_bytes = await file.read()
    file_hash = hashlib.sha256(file_content_bytes).hexdigest()

    client = MongoClient(settings.MONGO_URI)
    db = client.file_database

    existing_upload = db.upload_history.find_one({
        "file_hash": file_hash,
        "status": "completed"
    })
    if existing_upload:
        client.close()
        raise HTTPException(status_code=409, detail="Este arquivo já foi enviado e processado anteriormente.")

    history_entry = {
        "filename": file.filename,
        "upload_date": datetime.utcnow(),
        "status": "pending",
        "file_hash": file_hash,
        "content_type": file.content_type
    }
    result = db.upload_history.insert_one(history_entry)
    upload_id = str(result.inserted_id)
    client.close()

    process_file_task.delay(upload_id, file_content_bytes, file.content_type)

    return {"message": "Arquivo recebido e agendado para processamento.", "upload_id": upload_id}