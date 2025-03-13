"""
Main entry point for the FastAPI application.
It includes the router defined in /src/api/v1/endpoint1/endpoint1.py.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.api.v1.router import router as v1_router
from src.middleware import logging_middleware

app = FastAPI(
    title="Real-Time Data Processing API",
    description="ASGI-based service for ingesting, processing, and querying data.",
    version="1.0.0"
)

# Add middleware
app.middleware("http")(logging_middleware)

# Global error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )

# Include the v1 router
app.include_router(v1_router, prefix="/api/v1", tags=["v1"])
