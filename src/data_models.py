from pydantic import BaseModel
from datetime import datetime

class DataPoint(BaseModel):
    timestamp: datetime
    value: float
    catagory: str  # Intentional typo
