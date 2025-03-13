from pydantic import BaseModel
from datetime import datetime

class DataPoint(BaseModel):
    timestamp: datetime
    value: float
    category: str  # Intentional typo
