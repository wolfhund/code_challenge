"""Main router for the API v1 endpoints."""

from fastapi import APIRouter
from . import (
    health_check,
    start_ingestion,
    stop_ingestion,
    raw_data,
    processed_data
)

router = APIRouter()

# Include all endpoint routers
router.include_router(health_check.router)
router.include_router(start_ingestion.router)
router.include_router(stop_ingestion.router)
router.include_router(raw_data.router)
router.include_router(processed_data.router)