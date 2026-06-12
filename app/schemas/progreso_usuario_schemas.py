"""
Schemas para ProgresoUsuario.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.schemas.base import TipoActividadEnum


class ProgresoUsuarioCreateSchema(BaseModel):
    """Registrar nueva actividad completada."""
    tipo_actividad: TipoActividadEnum
    referencia_id: UUID
    tipo_referencia: str = Field(..., max_length=50)
    duracion_real_segundos: int | None = None
    completado: bool = True
    porcentaje_completado: int = Field(100, ge=0, le=100)
    notas: str | None = None


class ProgresoUsuarioResponse(BaseModel):
    """Respuesta de progreso."""
    id: UUID
    dispositivo_id: UUID
    tipo_actividad: str
    referencia_id: UUID
    duracion_real_segundos: int | None = None
    completado: bool
    porcentaje_completado: int
    puntos_ganados: int
    realizado_en: datetime

    class Config:
        from_attributes = True


class ProgresoUsuarioListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[ProgresoUsuarioResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool