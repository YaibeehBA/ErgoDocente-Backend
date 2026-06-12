"""
Schemas para CategoriaEjercicio.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CategoriaEjercicioResponse(BaseModel):
    """Respuesta de categoría de ejercicio."""
    id: UUID
    slug: str
    icono_url: str | None = None
    color_hex: str = Field(..., pattern=r'^#[0-9A-F]{6}$')
    orden: int
    esta_activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True


class CategoriasEjerciciosListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[CategoriaEjercicioResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool