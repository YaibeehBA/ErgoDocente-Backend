"""
Schemas para EnfermedadOcupacional.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class EnfermedadOcupacionalResponse(BaseModel):
    """Respuesta de enfermedad ocupacional."""
    id: UUID
    slug: str
    categoria: str
    codigo_cie10: str | None = None
    esta_publicado: bool
    archivo_media_id: UUID | None = None
    creado_en: datetime

    class Config:
        from_attributes = True


class EnfermedadesOcupacionalesListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[EnfermedadOcupacionalResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool