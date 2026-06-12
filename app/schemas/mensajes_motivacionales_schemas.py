"""
Schemas para MensajeMotivacional.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class MensajeMotivacionalResponse(BaseModel):
    """Respuesta de mensaje motivacional."""
    id: UUID
    autor: str | None = None
    categoria: str
    esta_publicado: bool
    creado_en: datetime

    class Config:
        from_attributes = True


class MensajesMotivacionalesListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[MensajeMotivacionalResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool