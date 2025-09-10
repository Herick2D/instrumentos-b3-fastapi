from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UploadHistory(BaseModel):
    filename: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "processando"
    record_count: Optional[int] = None
    error: Optional[str] = None

class StockData(BaseModel):
    RptDt: str = Field(..., alias="RptDt")
    TckrSymb: str = Field(..., alias="TckrSymb")
    MktNm: str = Field(..., alias="MktNm")
    SctyCtgyNm: str = Field(..., alias="SctyCtgyNm")
    ISIN: str = Field(..., alias="ISIN")
    CrpnNm: str = Field(..., alias="CrpnNm")

    class Config:
        allow_population_by_field_name = True
