"""Middleware for request logging and error handling."""

from fastapi import Request
import logging
from time import time
from typing import Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next: Callable):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {process_time:.3f}s"
    )
    return response