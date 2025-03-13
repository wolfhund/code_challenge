"""Stop ingestion endpoint for the data ingestion pipeline."""

from fastapi import APIRouter
from src.data_models import IngestionStopResponse
from src.ingestion import stop_data_ingestion

router = APIRouter()

@router.post("/stop-ingestion", response_model=IngestionStopResponse)
async def stop_ingestion() -> IngestionStopResponse:
    """
    Stops the ingestion process if it is running.
    """
    # Stop ingestion
    await stop_data_ingestion()
    return IngestionStopResponse(message="Data ingestion stopped.")