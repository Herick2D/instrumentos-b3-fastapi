from fastapi import FastAPI
from routers import upload, history, content

app = FastAPI(
    title="Instrumentos B3 API",
    description="API para upload e consulta de arquivos de dados financeiros.",
    version="1.0.0"
)

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(history.router, prefix="/api", tags=["History"])
app.include_router(content.router, prefix="/api", tags=["Content"])

@app.get("/")
def read_root():
    return {"message": "Bem vindo!"}