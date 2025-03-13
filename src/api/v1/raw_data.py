"""Raw data endpoint for the data ingestion pipeline."""

from fastapi import APIRouter
from typing import List
from src.data_models import DataItem
from src.ingestion import RAW_DATA_STORAGE

router = APIRouter()

@router.get("/raw-data", response_model=List[DataItem])
async def get_raw_data() -> List[DataItem]:
    """
    Returns all raw data items that have been ingested so far.
    """
    return RAW_DATA_STORAGE