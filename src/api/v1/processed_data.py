"""Processed data endpoint for the data ingestion pipeline."""

from fastapi import APIRouter, HTTPException, status
from typing import List
from src.data_models import ProcessedItem
from src.ingestion import RAW_DATA_STORAGE
from src.data_pipeline import process_data

router = APIRouter()

@router.get("/processed-data", response_model=List[ProcessedItem])
async def get_processed_data() -> List[ProcessedItem]:
    """
    Returns processed data after applying various pandas transformations.
    """
    if not RAW_DATA_STORAGE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data available to process."
        )

    # Process the raw data
    processed = process_data(RAW_DATA_STORAGE)
    return processed