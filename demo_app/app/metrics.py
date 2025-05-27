"""Prometheus metrics for the demo application."""

import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware


# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

ERROR_COUNT = Counter(
    'http_errors_total',
    'Total number of HTTP errors',
    ['method', 'endpoint', 'status_code']
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics for HTTP requests."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Get method and path
        method = request.method
        path = request.url.path
        
        # Process the request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Record metrics
        status_code = str(response.status_code)
        
        REQUEST_COUNT.labels(
            method=method,
            endpoint=path,
            status_code=status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=method,
            endpoint=path
        ).observe(duration)
        
        # Track errors (4xx and 5xx)
        if response.status_code >= 400:
            ERROR_COUNT.labels(
                method=method,
                endpoint=path,
                status_code=status_code
            ).inc()
        
        return response


def instrument_app(app: FastAPI) -> None:
    """Add Prometheus instrumentation to a FastAPI app."""
    app.add_middleware(PrometheusMiddleware)


def metrics_handler() -> Response:
    """Return Prometheus metrics in the expected format."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
