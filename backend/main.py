from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config.settings import settings
from backend.routes.auth import router as auth_router
from backend.routes.dataset import router as dataset_router
from backend.routes.ai import router as ai_router
from backend.utils.database import create_db_and_tables
from backend.utils.exceptions import NeuroSyncException
from backend.utils.logger import logger


app = FastAPI(title="NeuroSync API", version="2.1.0")


@app.on_event("startup")
def startup_event():
    logger.info("Starting NeuroSync.")
    create_db_and_tables()
    logger.info("Database initialized successfully.")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning("HTTP %s on %s: %s", exc.status_code, request.url.path, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": str(exc.detail)},
    )


@app.exception_handler(NeuroSyncException)
async def neurosync_exception_handler(request: Request, exc: NeuroSyncException):
    logger.error("Domain error on %s: %s", request.url.path, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.message},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex=settings.ALLOWED_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(dataset_router)
app.include_router(ai_router)


@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "NeuroSync API healthy",
        "data": {"service": "NeuroSync", "version": "2.1.0"},
    }


@app.get("/")
def root():
    return {
        "success": True,
        "message": "NeuroSync API Running",
        "data": None,
    }
