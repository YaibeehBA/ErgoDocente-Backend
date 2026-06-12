"""
Schemas para EjercicioRutina (pivote con datos).
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class EjercicioRutinaResponse(BaseModel):
    """Respuesta de ejercicio en rutina."""
    id: UUID
    rutina_id: UUID
    ejercicio_id: UUID
    orden: int
    duracion_segundos_override: int | None = None
    repeticiones_override: int | None = None
    descanso_segundos: int
    es_obligatorio: bool
    creado_en: datetime

    class Config:
        from_attributes = True


class EjercicioRutinaListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[EjercicioRutinaResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool