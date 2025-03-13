"""
Data models and Pydantic schemas used throughout the application.
"""

from datetime import datetime
from pydantic import BaseModel, Field

class DataItem(BaseModel):
    """
    Represents a single data point in our system.
    """
    id: int
    timestamp: datetime
    value_a: float
    value_b: float

class ProcessedItem(BaseModel):
    """
    Represents a processed data record after transformations.
    """
    id: int
    name: str
    metric: str
    mean_value: float

class IngestionStartResponse(BaseModel):
    """
    Response returned when ingestion starts.
    """
    message: str

class IngestionStopResponse(BaseModel):
    """
    Response returned when ingestion stops.
    """
    message: str

class HealthCheckResponse(BaseModel):
    """
    Response for a health-check endpoint.
    """
    status: str
    message: str
