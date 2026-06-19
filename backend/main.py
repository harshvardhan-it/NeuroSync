from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.auth import router as auth_router
from backend.routes.dataset import router as dataset_router
from backend.utils.database import create_db_and_tables
from backend.utils.logger import logger
from backend.routes.ai import (
    router as ai_router
)


app = FastAPI(
    title="NeuroSync API",
    version="1.0.0"
)

create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
            "error": exc.detail,
        },
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
            "error": "Internal server error",
        },
    )


app.include_router(auth_router)
app.include_router(dataset_router)
app.include_router(ai_router)

@app.get("/")
def root():

    logger.info(
        "Root endpoint accessed"
    )

    return {
        "success": True,
        "message": "NeuroSync API Running",
        "data": None,
    }