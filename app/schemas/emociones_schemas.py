"""
Schemas para Emoción.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class EmocionResponse(BaseModel):
    """Respuesta de emoción."""
    id: UUID
    slug: str
    emoji: str = Field(..., max_length=10)
    color_hex: str = Field(..., pattern=r'^#[0-9A-F]{6}$')
    nivel_intensidad: int = Field(..., ge=1, le=5)
    es_positiva: bool
    esta_activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True


class EmocionesListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[EmocionResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool