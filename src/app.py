from .middleware import error_handler
from fastapi import FastAPI
from .ingestion import DataIngestion
from .data_pipeline import process_data
import asyncio

app = FastAPI()
app.middleware("http")(error_handler)
ingestion = DataIngestion()

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/start-ingestion")
async def start_ingestion():
    asyncio.create_task(ingestion.start())
    return {"message": "Data ingestion started"}

@app.post("/api/v1/stop-ingestion")
def stop_ingestion():
    ingestion.stop()
    return {"message": "Data ingestion stopped"}

@app.get("/api/v1/raw-data")
def get_raw_data():
    return ingestion.data

@app.get("/api/v1/processed-data")
def get_processed_data():
    return process_data(ingestion.data)
