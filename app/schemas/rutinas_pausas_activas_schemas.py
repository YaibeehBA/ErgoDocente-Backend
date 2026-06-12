"""
Schemas para RutinaPausaActiva.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class RutinaPausaActivaResponse(BaseModel):
    """Respuesta de rutina de pausa activa."""
    id: UUID
    slug: str
    duracion_total_minutos: int
    nivel_dificultad: str
    esta_publicado: bool
    es_predeterminado: bool
    esta_destacado: bool
    veces_completada: int
    archivo_media_id: UUID | None = None
    creado_en: datetime

    class Config:
        from_attributes = True


class RutinasListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[RutinaPausaActivaResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool