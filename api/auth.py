 
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import get_settings

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

settings = get_settings()

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Falha na validação das credenciais",
        )