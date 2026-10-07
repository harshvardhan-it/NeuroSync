from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config.settings import settings
from backend.routes.ai import router as ai_router
from backend.routes.auth import router as auth_router
from backend.routes.dataset import router as dataset_router
from backend.utils.database import create_db_and_tables, engine
from backend.utils.exceptions import (
    NeuroSyncException,
    generic_exception_handler,
    neurosync_exception_handler,
)
from backend.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting NeuroSync...")
    create_db_and_tables()
    logger.info("Database initialized successfully.")
    yield
    engine.dispose()
    logger.info("NeuroSync shutdown complete.")


app = FastAPI(
    title="NeuroSync API",
    version="2.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(NeuroSyncException)
async def handle_neurosync_exception(request: Request, exc: NeuroSyncException):
    return await neurosync_exception_handler(request, exc)


@app.exception_handler(HTTPException)
async def handle_http_exception(request: Request, exc: HTTPException):
    logger.warning("HTTP %s %s: %s", request.method, request.url.path, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": str(exc.detail),
            },
        },
    )


@app.exception_handler(Exception)
async def handle_unhandled_exception(request: Request, exc: Exception):
    logger.exception(
        "Unhandled exception method=%s path=%s",
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred.",
            },
        },
    )


app.include_router(auth_router)
app.include_router(dataset_router)
app.include_router(ai_router)


@app.get("/health/live", tags=["Health"])
def liveness():
    return {"status": "ok", "service": "NeuroSync"}


@app.get("/health/ready", tags=["Health"])
def readiness():
    try:
        with engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
        return {"status": "ready", "service": "NeuroSync"}
    except Exception:
        logger.exception("Readiness check failed.")
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "service": "NeuroSync"},
        )


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "NeuroSync", "version": app.version}


@app.get("/")
def root():
    return {
        "success": True,
        "message": "NeuroSync API Running",
        "data": {"version": app.version},
    }
