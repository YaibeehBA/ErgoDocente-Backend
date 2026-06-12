"""
Schemas para Recordatorio.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, time
from app.schemas.base import TipoRecordatorioEnum


class RecordatorioCreateSchema(BaseModel):
    """Crear recordatorio."""
    titulo: str = Field(..., max_length=255)
    mensaje: str | None = None
    tipo: TipoRecordatorioEnum
    hora: time
    dias_semana: list[int] = Field(..., description="[1,2,3,4,5] = Lun-Vie")
    rutina_sugerida_id: UUID | None = None


class RecordatorioUpdateSchema(BaseModel):
    """Actualizar recordatorio."""
    titulo: str | None = Field(None, max_length=255)
    mensaje: str | None = None
    hora: time | None = None
    dias_semana: list[int] | None = None
    esta_activo: bool | None = None
    rutina_sugerida_id: UUID | None = None


class RecordatorioResponse(BaseModel):
    """Respuesta de recordatorio."""
    id: UUID
    dispositivo_id: UUID
    titulo: str
    mensaje: str | None
    tipo: str
    hora: time
    dias_semana: list[int]
    esta_activo: bool
    rutina_sugerida_id: UUID | None = None
    creado_en: datetime

    class Config:
        from_attributes = True


class RecordatoriosListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[RecordatorioResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool