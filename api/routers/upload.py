from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, status
from pymongo import MongoClient
from datetime import datetime
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
    allowed_content_types = [
        'text/csv',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]
    if file.content_type not in allowed_content_types:
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Apenas Excel e CSV são permitidos.")

    client = MongoClient(settings.MONGO_URI)
    db = client.file_database

    if db.upload_history.find_one({"filename": file.filename}):
        client.close()
        raise HTTPException(status_code=409, detail="Já existe um arquivo com este nome.")

    history_entry = {
        "filename": file.filename,
        "upload_date": datetime.utcnow(),
        "status": "processing",
        "content_type": file.content_type
    }
    db.upload_history.insert_one(history_entry)
    client.close()

    file_content_bytes = await file.read()

    process_file_task.delay(file_content_bytes, file.filename, file.content_type)

    return {"message": "Arquivo recebido e em processamento.", "filename": file.filename}

