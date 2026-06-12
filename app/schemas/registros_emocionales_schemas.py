"""
Schemas para RegistroEmocional.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class RegistroEmocionalCreateSchema(BaseModel):
    """Registrar emoción."""
    emocion_id: UUID
    intensidad: int = Field(..., ge=1, le=5)
    contexto: str | None = Field(None, max_length=100)
    notas: str | None = None
    ubicacion_cuerpo: str | None = Field(None, max_length=100)


class RegistroEmocionalResponse(BaseModel):
    """Respuesta de registro emocional."""
    id: UUID
    dispositivo_id: UUID
    emocion_id: UUID
    intensidad: int
    contexto: str | None
    notas: str | None
    ubicacion_cuerpo: str | None = None
    registrado_en: datetime

    class Config:
        from_attributes = True


class RegistrosEmocionalListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[RegistroEmocionalResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool