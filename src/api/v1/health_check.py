"""Health check endpoint for the data ingestion pipeline."""

from fastapi import APIRouter
from src.data_models import HealthCheckResponse

router = APIRouter()

@router.get("/health-check", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Simple health-check endpoint to verify that the service is running.
    """
    return HealthCheckResponse(status="ok", message="Service is up and running!")