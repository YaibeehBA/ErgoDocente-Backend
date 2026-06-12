"""
Schemas para Consejo.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ConsejoResponse(BaseModel):
    """Respuesta de consejo."""
    id: UUID
    slug: str
    categoria: str
    esta_publicado: bool
    orden: int
    archivo_media_id: UUID | None = None
    creado_en: datetime

    class Config:
        from_attributes = True


class ConsejosListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[ConsejoResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool