import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor

from app.core.config import settings


def _agregar_severidad(
    logger: Any, method: str, event_dict: EventDict
) -> EventDict:
    """
    Agrega campo 'severity' compatible con Google Cloud Logging / Datadog.
    """
    level = event_dict.get("level", method).upper()
    event_dict["severity"] = level
    return event_dict


def _quitar_color_en_json(
    logger: Any, method: str, event_dict: EventDict
) -> EventDict:
    """Limpia markup de colores ANSI cuando el destino es JSON."""
    if settings.LOG_FORMAT == "json":
        event_dict.pop("_record", None)
        event_dict.pop("_from_structlog", None)
    return event_dict


def setup_logging() -> None:
    """
    Configura structlog según el entorno.
    - development/testing → ConsoleRenderer (colores, legible)
    - staging/production  → JSONRenderer (logs para ingestión)
    """
    nivel = getattr(logging, settings.LOG_LEVEL, logging.INFO)

    # Procesadores compartidos
    # DESPUÉS - correcto
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,         
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        _agregar_severidad,
    ]

    if settings.LOG_FORMAT == "json" or settings.es_produccion:
        # Producción: JSON estructurado
        renderer: Processor = structlog.processors.JSONRenderer()
    else:
        # Desarrollo: legible con colores
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(nivel),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )

    # Integrar logging estándar de Python
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=nivel,
    )

    # Silenciar loggers ruidosos
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DEBUG else logging.WARNING
    )
    logging.getLogger("asyncpg").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


def get_logger(nombre: str) -> structlog.BoundLogger:
    """Atajo para obtener un logger con nombre de módulo."""
    return structlog.get_logger(nombre)