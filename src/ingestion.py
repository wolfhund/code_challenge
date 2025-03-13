"""
Handles the asynchronous ingestion of data.
Uses a background task that generates random data and stores it.
"""

import asyncio
import random
from datetime import datetime
from typing import List, Optional

from src.data_models import DataItem

# Global variables for simplicity (avoid in production; use DB or caching layer).
RAW_DATA_STORAGE: List[DataItem] = []
INGESTION_TASK: Optional[asyncio.Task] = None
INGESTION_RUNNING: bool = False

async def start_data_ingestion(interval: float = 2.0) -> None:
    """
    Starts an asynchronous task that periodically generates random data and stores it.
    :param interval: Interval in seconds between data generation.
    """
    global INGESTION_RUNNING, INGESTION_TASK

    if INGESTION_RUNNING:
        # Already running, do nothing or raise an exception
        return

    INGESTION_RUNNING = True

    async def _ingest_loop() -> None:
        """
        Internal loop that runs until the task is canceled or ingestion is stopped.
        """
        try:
            while True:
                # Generate a random DataItem
                new_item = DataItem(
                    id=random.randint(0, 9),  # 0 to 9
                    timestamp=datetime.utcnow(),
                    value_a=round(random.uniform(1.0, 5.0), 2),
                    value_b=round(random.uniform(1.0, 5.0), 2)
                )
                RAW_DATA_STORAGE.append(new_item)
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            # Task was canceled, clean up if needed
            raise

    # Create a background task
    INGESTION_TASK = asyncio.create_task(_ingest_loop())

async def stop_data_ingestion() -> None:
    """
    Stops the data ingestion task if it is running.
    """
    global INGESTION_RUNNING, INGESTION_TASK

    if not INGESTION_RUNNING or INGESTION_TASK is None:
        # Nothing to stop
        return

    INGESTION_RUNNING = False
    if not INGESTION_TASK.done():
        INGESTION_TASK.cancel()
        try:
            await INGESTION_TASK
        except asyncio.CancelledError:
            # Expected when we cancel the task
            pass
    INGESTION_TASK = None
