"""
Schemas para sistema polimórfico de traducciones.
Tabla única: tabla, registro_id, campo, idioma_id → valor
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class TraduccionCreateSchema(BaseModel):
    """Crear traducción (admin only)."""
    tabla: str = Field(..., max_length=100, description="ejercicios, rutinas, etc.")
    registro_id: UUID = Field(..., description="UUID del registro a traducir")
    campo: str = Field(..., max_length=100, description="titulo, descripcion, etc.")
    idioma_id: UUID
    valor: str = Field(..., min_length=1, max_length=10000)


class TraduccionUpdateSchema(BaseModel):
    """Actualizar traducción."""
    valor: str = Field(..., min_length=1, max_length=10000)


class TraduccionResponse(BaseModel):
    """Respuesta de traducción."""
    id: UUID
    tabla: str
    registro_id: UUID
    campo: str
    idioma_id: UUID
    valor: str
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


class TraduccionesListResponse(BaseModel):
    """Respuesta paginada de traducciones."""
    items: list[TraduccionResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool