from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UploadHistory(BaseModel):
    filename: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"
    file_hash: str
    record_count: Optional[int] = 0
    error: Optional[str] = None

class StockData(BaseModel):
    RptDt: Optional[str] = None
    TckrSymb: Optional[str] = None
    MktNm: Optional[str] = None
    SctyCtgyNm: Optional[str] = None
    ISIN: Optional[str] = None
    CrpnNm: Optional[str] = None

    class Config:
        from_attributes = True

