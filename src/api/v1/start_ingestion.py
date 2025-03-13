"""Start ingestion endpoint for the data ingestion pipeline."""

from fastapi import APIRouter, HTTPException, status
from src.data_models import IngestionStartResponse
from src.ingestion import start_data_ingestion, INGESTION_RUNNING

router = APIRouter()

@router.post("/start-ingestion", response_model=IngestionStartResponse)
async def start_ingestion(interval: float = 2.0) -> IngestionStartResponse:
    """
    Starts the ingestion process if not already running.
    Optional query parameter 'interval' to specify generation interval.
    """
    if INGESTION_RUNNING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data ingestion is already running."
        )
    # Start ingestion
    await start_data_ingestion(interval=interval)
    return IngestionStartResponse(message="Data ingestion started.")