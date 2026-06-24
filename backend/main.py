from fastapi import FastAPI
from fastapi import Request
from fastapi import HTTPException

from fastapi.responses import JSONResponse

from fastapi.middleware.cors import (
    CORSMiddleware
)

from backend.routes.auth import (
    router as auth_router
)

from backend.routes.dataset import (
    router as dataset_router
)

from backend.routes.ai import (
    router as ai_router
)

from backend.utils.database import (
    create_db_and_tables
)

from backend.utils.logger import (
    logger
)

from backend.utils.exceptions import (
    NeuroSyncException,
    neurosync_exception_handler,
    generic_exception_handler
)

from backend.config.settings import (
    settings
)


app = FastAPI(
    title="NeuroSync API",
    version="2.0.0"
)

# ==========================================================
# STARTUP
# ==========================================================

@app.on_event("startup")
def startup_event():

    logger.info(
        "Starting NeuroSync..."
    )

    create_db_and_tables()

    logger.info(
        "Database initialized successfully."
    )

# ==========================================================
# EXCEPTION HANDLERS
# ==========================================================

app.add_exception_handler(
    NeuroSyncException,
    neurosync_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    logger.warning(
        f"HTTP {exc.status_code}: {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(
        f"Unhandled exception: {str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error"
        }
    )

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================================
# ROUTERS
# ==========================================================

app.include_router(auth_router)

app.include_router(dataset_router)

app.include_router(ai_router)

# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "NeuroSync",
        "version": "2.0.0"
    }

# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def root():

    logger.info(
        "Root endpoint accessed"
    )

    return {
        "success": True,
        "message": "NeuroSync API Running",
        "data": None
    }