"""
Schemas para ContenidoErgonomico.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ContenidoErgonomicoResponse(BaseModel):
    """Respuesta de contenido ergonómico."""
    id: UUID
    slug: str
    tipo: str
    nivel_dificultad: str
    tiempo_lectura_minutos: int
    orden: int
    esta_publicado: bool
    esta_destacado: bool
    vistas: int
    archivo_media_id: UUID | None = None
    creado_en: datetime

    class Config:
        from_attributes = True


class ContenidosErgonomicosListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[ContenidoErgonomicoResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool