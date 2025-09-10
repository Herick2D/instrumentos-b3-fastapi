import redis
import json
from fastapi import APIRouter, Query
from typing import Optional
from pymongo import MongoClient

from api.config import get_settings
from api.models import StockData

router = APIRouter()
settings = get_settings()

redis_client = redis.Redis.from_url(settings.REDIS_URI, decode_responses=True)


@router.get("/content", response_model=list[StockData])
def get_file_content(
        TckrSymb: Optional[str] = Query(None, description="Filtrar por símbolo do ticker"),
        RptDt: Optional[str] = Query(None, description="Filtrar por data do relatório (YYYY-MM-DD)"),
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
):
    cache_key = f"content_query:{TckrSymb}:{RptDt}:{page}:{page_size}"

    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    client = MongoClient(settings.MONGO_URI)
    db = client.file_database

    query = {}
    if TckrSymb:
        query["TckrSymb"] = TckrSymb
    if RptDt:
        query["RptDt"] = RptDt

    skip = (page - 1) * page_size
    cursor = db.file_content.find(query, {"_id": 0}).skip(skip).limit(page_size)
    results = list(cursor)
    client.close()

    redis_client.set(cache_key, json.dumps(results), ex=300)

    return results
