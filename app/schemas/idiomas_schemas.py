"""
Schemas para Idioma - catálogo de idiomas (Español, Kichwa).
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class IdiomaResponse(BaseModel):
    """Respuesta de idioma."""
    id: UUID
    codigo: str = Field(..., description="Código ISO: es, kw")
    nombre: str
    nombre_en_espanol: str
    bandera_emoji: str | None = None
    es_predeterminado: bool
    esta_activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True


class IdiomasListResponse(BaseModel):
    """Respuesta de listado de idiomas."""
    items: list[IdiomaResponse]
    total: int