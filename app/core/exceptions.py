from typing import Any

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

logger = structlog.get_logger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
# ══════════════════════════════════════════════════════════════════════════════

class ErgoDocenteException(Exception):
    """Excepción base de la aplicación."""

    def __init__(
        self,
        mensaje: str,
        codigo: str = "ERROR_INTERNO",
        datos: dict[str, Any] | None = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        self.mensaje = mensaje
        self.codigo = codigo
        self.datos = datos or {}
        self.status_code = status_code
        super().__init__(mensaje)


class RecursoNoEncontradoError(ErgoDocenteException):
    """El recurso solicitado no existe o fue eliminado."""

    def __init__(self, recurso: str, identificador: Any = None) -> None:
        msg = f"{recurso} no encontrado"
        if identificador:
            msg = f"{recurso} con id '{identificador}' no encontrado"
        super().__init__(
            mensaje=msg,
            codigo="RECURSO_NO_ENCONTRADO",
            datos={"recurso": recurso, "id": str(identificador) if identificador else None},
            status_code=status.HTTP_404_NOT_FOUND,
        )


class ConflictoError(ErgoDocenteException):
    """El recurso ya existe (duplicado)."""

    def __init__(self, mensaje: str, campo: str | None = None) -> None:
        super().__init__(
            mensaje=mensaje,
            codigo="CONFLICTO",
            datos={"campo": campo} if campo else {},
            status_code=status.HTTP_409_CONFLICT,
        )


class ValidacionError(ErgoDocenteException):
    """Error de validación de negocio (diferente a validación Pydantic)."""

    def __init__(self, mensaje: str, campo: str | None = None) -> None:
        super().__init__(
            mensaje=mensaje,
            codigo="ERROR_VALIDACION",
            datos={"campo": campo} if campo else {},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class AccesoDenegadoError(ErgoDocenteException):
    """Sin permiso para ejecutar esta acción (preparado para V2 auth)."""

    def __init__(self, accion: str = "realizar esta acción") -> None:
        super().__init__(
            mensaje=f"No tiene permiso para {accion}",
            codigo="ACCESO_DENEGADO",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class DispositivoNoRegistradoError(ErgoDocenteException):
    """El device_id no está registrado en el sistema."""

    def __init__(self, device_id: str) -> None:
        super().__init__(
            mensaje=f"Dispositivo '{device_id}' no registrado. Registre el dispositivo primero.",
            codigo="DISPOSITIVO_NO_REGISTRADO",
            datos={"device_id": device_id},
            status_code=status.HTTP_404_NOT_FOUND,
        )


class CloudinaryError(ErgoDocenteException):
    """Error al interactuar con Cloudinary."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(
            mensaje=f"Error en servicio de medios: {mensaje}",
            codigo="ERROR_CLOUDINARY",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


class HeaderRequeridoError(ErgoDocenteException):
    """Header obligatorio ausente en la petición."""

    def __init__(self, header: str) -> None:
        super().__init__(
            mensaje=f"Header requerido ausente: '{header}'",
            codigo="HEADER_REQUERIDO",
            datos={"header": header},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ══════════════════════════════════════════════════════════════════════════════
# FORMATO DE RESPUESTA DE ERROR ESTÁNDAR
# ══════════════════════════════════════════════════════════════════════════════

def _respuesta_error(
    status_code: int,
    codigo: str,
    mensaje: str,
    datos: dict | None = None,
) -> JSONResponse:
    """Construye una respuesta JSON de error con formato uniforme."""
    return JSONResponse(
        status_code=status_code,
        content={
            "exito": False,
            "error": {
                "codigo": codigo,
                "mensaje": mensaje,
                "datos": datos or {},
            },
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
# MANEJADORES GLOBALES DE EXCEPCIONES
# ══════════════════════════════════════════════════════════════════════════════

async def manejar_excepcion_app(
    request: Request, exc: ErgoDocenteException
) -> JSONResponse:
    logger.warning(
        "Excepción de aplicación",
        codigo=exc.codigo,
        mensaje=exc.mensaje,
        path=request.url.path,
        method=request.method,
    )
    return _respuesta_error(exc.status_code, exc.codigo, exc.mensaje, exc.datos)


async def manejar_validacion_pydantic(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errores = []
    for error in exc.errors():
        errores.append({
            "campo": " → ".join(str(loc) for loc in error["loc"]),
            "mensaje": error["msg"],
            "tipo": error["type"],
        })
    logger.warning(
        "Error de validación Pydantic",
        errores=errores,
        path=request.url.path,
    )
    return _respuesta_error(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        codigo="ERROR_VALIDACION_ENTRADA",
        mensaje="Los datos enviados no son válidos",
        datos={"errores": errores},
    )


async def manejar_integridad_db(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    logger.error(
        "Error de integridad en base de datos",
        error=str(exc.orig),
        path=request.url.path,
    )
    # Detectar tipo de violación
    msg_orig = str(exc.orig).lower() if exc.orig else ""
    if "unique" in msg_orig or "duplicate" in msg_orig:
        codigo = "REGISTRO_DUPLICADO"
        mensaje = "Ya existe un registro con esos datos"
    elif "foreign key" in msg_orig:
        codigo = "REFERENCIA_INVALIDA"
        mensaje = "El registro referenciado no existe"
    else:
        codigo = "ERROR_INTEGRIDAD_DB"
        mensaje = "Error de integridad en la base de datos"

    return _respuesta_error(
        status_code=status.HTTP_409_CONFLICT,
        codigo=codigo,
        mensaje=mensaje,
    )


async def manejar_error_sqlalchemy(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    logger.error(
        "Error SQLAlchemy inesperado",
        error=str(exc),
        path=request.url.path,
    )
    return _respuesta_error(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        codigo="ERROR_BASE_DATOS",
        mensaje="Error temporal en la base de datos. Reintente.",
    )


async def manejar_error_generico(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception(
        "Error inesperado no manejado",
        error=str(exc),
        path=request.url.path,
        method=request.method,
    )
    return _respuesta_error(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        codigo="ERROR_INTERNO_SERVIDOR",
        mensaje="Ocurrió un error inesperado. El equipo ha sido notificado.",
    )

def configure_exception_handlers(app: FastAPI) -> None:
    """Registra todos los manejadores de excepciones en la app FastAPI."""
    app.add_exception_handler(ErgoDocenteException, manejar_excepcion_app)  # type: ignore
    app.add_exception_handler(RequestValidationError, manejar_validacion_pydantic)  # type: ignore
    app.add_exception_handler(IntegrityError, manejar_integridad_db)  # type: ignore
    app.add_exception_handler(SQLAlchemyError, manejar_error_sqlalchemy)  # type: ignore
    app.add_exception_handler(Exception, manejar_error_generico)  # type: ignore