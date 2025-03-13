import asyncio
import random
from datetime import datetime
from .data_models import DataPoint

class DataIngestion:
    def __init__(self):
        self._running = False
        self.data = []
    
    async def start(self):
        self._running = True
        while self._running:
            await self._generate_data()
            await asyncio.sleep(1)
    
    def stop(self):
        self._running = False
    
    async def _generate_data(self):
        point = DataPoint(
            timestamp=datetime.now(),
            value=random.uniform(0, 100),
            category=random.choice(["A", "B"])
        )
        self.data.append(point)
