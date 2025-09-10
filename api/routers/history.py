from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime
from pymongo import MongoClient
from bson import json_util
import json

from api.config import get_settings


router = APIRouter()
settings = get_settings()


@router.get("/history")
def get_upload_history(
        filename: Optional[str] = Query(None, description="Filtrar por nome do arquivo"),
        ref_date: Optional[datetime] = Query(None, description="Filtrar por data de referência (YYYY-MM-DD)"),
):
    client = MongoClient(settings.MONGO_URI)
    db = client.file_database

    query = {}
    if filename:
        query["filename"] = {"$regex": filename, "$options": "i"}
    if ref_date:
        start_of_day = datetime(ref_date.year, ref_date.month, ref_date.day)
        end_of_day = datetime(ref_date.year, ref_date.month, ref_date.day, 23, 59, 59)
        query["upload_date"] = {"$gte": start_of_day, "$lt": end_of_day}

    history = list(db.upload_history.find(query, {"_id": 0}))
    client.close()

    return json.loads(json_util.dumps(history))
