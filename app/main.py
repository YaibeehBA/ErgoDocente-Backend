"""
FastAPI application factory para ErgoDocente Backend.
"""
import time
import uuid
from contextlib import asynccontextmanager

import structlog
import structlog.contextvars  
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.core.database import AsyncSessionLocal  
from app.core.exceptions import configure_exception_handlers
from app.core.logging_config import setup_logging
from app.routers.v1 import routers

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de ciclo de vida."""
    # STARTUP
    setup_logging()
    logger.info("ergodocente_startup", mensaje="Iniciando ErgoDocente API...")

    _configurar_cloudinary()
    await _verificar_conexion_bd()

    logger.info(
        "ergodocente_listo",
        entorno=settings.APP_ENV,
        debug=settings.DEBUG,
        version="1.0.0",
    )

    yield

    # SHUTDOWN
    logger.info("ergodocente_shutdown", mensaje="Apagando ErgoDocente API...")


def _configurar_cloudinary() -> None:
    """Configurar Cloudinary."""
    try:
        import cloudinary  # type: ignore
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )
        logger.info("cloudinary_configurado", cloud=settings.CLOUDINARY_CLOUD_NAME)
    except Exception as e:
        logger.warning("cloudinary_no_configurado", error=str(e))


async def _verificar_conexion_bd() -> None:
    """Verificar conexion a BD al arrancar."""
    try:
        from sqlalchemy import text
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))
        logger.info("bd_conexion_ok")
    except Exception as e:
        logger.error("bd_conexion_error", error=str(e))


def create_app() -> FastAPI:
    """Crear instancia de FastAPI."""

    app = FastAPI(
        title="ErgoDocente API",
        description="Backend para app de ergonomia y bienestar para docentes.",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    _registrar_middleware(app)
    configure_exception_handlers(app)
    _registrar_routers(app)

    return app


def _registrar_middleware(app: FastAPI) -> None:
    """Registrar middlewares."""

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"],
    )

    # Trusted hosts (produccion)
    if settings.es_produccion:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_ORIGINS,
        )

    # Middleware de logging
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next) -> Response:
        """Log cada request con duracion."""
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # Clear y bind contextvars
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        device_id = request.headers.get("X-Device-ID", "")
        logger.info(
            "request_inicio",
            query_params=str(request.query_params) or None,
            device_id=device_id[:8] if device_id else None,
        )

        response = await call_next(request)

        duracion_ms = round((time.perf_counter() - start_time) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(duracion_ms)

        logger.info(
            "request_fin",
            status_code=response.status_code,
            duracion_ms=duracion_ms,
        )

        return response


def _registrar_routers(app: FastAPI) -> None:
    """Registrar routers bajo /api/v1."""
    for router in routers:
        app.include_router(router, prefix="/api/v1")


# Instancia global de la app
app = create_app()