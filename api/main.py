from fastapi import FastAPI
from api.routers.observability import router as observability_router

app = FastAPI(
    title="Data Observability Platform",
    description="Proactive monitoring of data quality & ingestion",
    version="1.0.0"
)

app.include_router(observability_router)

@app.get("/")
def root():
    return {"status": "ok"}
