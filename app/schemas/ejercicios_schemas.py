"""
Schemas para Ejercicio.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CategoriaEjercicioMini(BaseModel):
    """Versión compacta de categoría para nested response."""
    id: UUID
    slug: str
    color_hex: str

    class Config:
        from_attributes = True


class EjercicioResponse(BaseModel):
    """Respuesta de ejercicio."""
    id: UUID
    slug: str
    categoria_id: UUID
    duracion_segundos: int
    repeticiones: int | None = None
    series: int
    nivel_dificultad: str
    parte_cuerpo: str
    posicion_inicial: str | None = None
    requiere_material: bool
    esta_publicado: bool
    esta_destacado: bool
    archivo_media_id: UUID | None = None
    creado_en: datetime

    class Config:
        from_attributes = True


class EjerciciosListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[EjercicioResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool