"""
Schemas base reutilizables: paginación, respuestas genéricas, enums compartidos.
"""
from typing import Generic, TypeVar, Literal
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from enum import Enum

# TypeVar para genéricos
T = TypeVar('T')


# ══════════════════════════════════════════════════════════════════════════════
# ENUMS COMPARTIDOS
# ══════════════════════════════════════════════════════════════════════════════

class RolEnum(str, Enum):
    """Roles de usuario para autenticación V2."""
    ADMIN = "admin"
    USUARIO = "usuario"


class PlataformaEnum(str, Enum):
    """Plataforma del dispositivo."""
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"


class NivelExperienciaEnum(str, Enum):
    """Nivel de experiencia con ejercicios."""
    PRINCIPIANTE = "principiante"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"


class TemaEnum(str, Enum):
    """Tema de interfaz."""
    CLARO = "claro"
    OSCURO = "oscuro"
    SISTEMA = "sistema"


class TipoRecursoEnum(str, Enum):
    """Tipo de archivo multimedia."""
    IMAGEN = "imagen"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENTO = "documento"


class NivelDificultadEnum(str, Enum):
    """Nivel de dificultad de contenido/ejercicio."""
    BASICO = "basico"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"


class TipoActividadEnum(str, Enum):
    """Tipo de actividad registrada."""
    RUTINA = "rutina"
    EJERCICIO = "ejercicio"
    CONTENIDO = "contenido"


class TipoRecordatorioEnum(str, Enum):
    """Tipo de recordatorio."""
    PAUSA_ACTIVA = "pausa_activa"
    HIDRATACION = "hidratacion"
    POSTURA = "postura"
    RESPIRACION = "respiracion"
    PERSONALIZADO = "personalizado"


class AccionAuditoriaEnum(str, Enum):
    """Acciones auditadas."""
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


# ══════════════════════════════════════════════════════════════════════════════
# PAGINACIÓN
# ══════════════════════════════════════════════════════════════════════════════

class PaginationQuerySchema(BaseModel):
    """
    Parámetros de query para listados paginados.
    Se usa en los endpoint GET con ?page=1&page_size=20
    """
    page: int = Field(1, ge=1, description="Número de página (1-based)")
    page_size: int = Field(
        20,
        ge=1,
        le=100,
        description="Elementos por página (máximo 100)"
    )
    search: str | None = Field(
        None,
        max_length=255,
        description="Búsqueda de texto libre"
    )
    order_by: str = Field(
        "creado_en",
        description="Campo para ordenar"
    )
    order_direction: Literal["asc", "desc"] = Field(
        "desc",
        description="Dirección: ascendente o descendente"
    )
    incluir_eliminados: bool = Field(
        False,
        description="Incluir registros soft-deleted"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "page_size": 20,
                "order_by": "creado_en",
                "order_direction": "desc",
                "incluir_eliminados": False
            }
        }


class PaginationResponseSchema(BaseModel, Generic[T]):
    """
    Respuesta paginada genérica.
    Se usa para retornar listas con metadatos de paginación.
    """
    items: list[T] = Field(..., description="Items de la página actual")
    total: int = Field(..., ge=0, description="Total de elementos")
    page: int = Field(..., ge=1, description="Página actual")
    page_size: int = Field(..., ge=1, description="Elementos por página")
    pages: int = Field(..., ge=0, description="Total de páginas")
    has_next: bool = Field(..., description="Hay más páginas")

    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "pages": 5,
                "has_next": True
            }
        }


# ══════════════════════════════════════════════════════════════════════════════
# RESPUESTAS ESTÁNDAR
# ══════════════════════════════════════════════════════════════════════════════

class RespuestaExitosaSchema(BaseModel, Generic[T]):
    """Respuesta exitosa genérica."""
    exito: bool = True
    data: T
    mensaje: str = Field(default="Operación exitosa")


class RespuestaErrorSchema(BaseModel):
    """Respuesta de error (manajada por exception handlers)."""
    exito: bool = False
    error: dict = Field(
        ...,
        description="error={codigo, mensaje, datos}"
    )