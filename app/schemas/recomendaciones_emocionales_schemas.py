"""
Schemas para RecomendacionEmocional.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class RecomendacionEmocionalCreateSchema(BaseModel):
    """Crear recomendación emocional."""
    emocion_id: UUID
    tipo_recomendacion: str = Field(..., max_length=50)
    referencia_id: UUID
    razon: str | None = None
    prioridad: int = Field(1, ge=1)


class RecomendacionEmocionalResponse(BaseModel):
    """Respuesta de recomendación."""
    id: UUID
    emocion_id: UUID
    tipo_recomendacion: str
    referencia_id: UUID
    razon: str | None
    prioridad: int
    creado_en: datetime

    class Config:
        from_attributes = True


class RecomendacionesEmocionalListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[RecomendacionEmocionalResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool