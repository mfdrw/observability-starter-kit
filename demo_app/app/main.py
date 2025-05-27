"""FastAPI demo application with Prometheus metrics."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .metrics import instrument_app, metrics_handler

# Create FastAPI instance
app = FastAPI(
    title="Observability Demo App",
    description="A simple FastAPI application for demonstrating observability tools",
    version="1.0.0"
)

# Add Prometheus instrumentation
instrument_app(app)


@app.get("/ping")
async def ping() -> JSONResponse:
    """Health check endpoint that returns a simple pong response."""
    return JSONResponse(
        content={"pong": True, "message": "Service is healthy"},
        status_code=200
    )


@app.get("/error")
async def error() -> None:
    """Endpoint that intentionally raises a 500 error for testing alerts."""
    raise HTTPException(
        status_code=500,
        detail="This is an intentional error for testing purposes"
    )


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return metrics_handler()


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint with basic information about the service."""
    return JSONResponse(
        content={
            "service": "observability-demo-app",
            "version": "1.0.0",
            "endpoints": {
                "health": "/ping",
                "error": "/error",
                "metrics": "/metrics"
            }
        },
        status_code=200
    )
