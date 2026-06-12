"""
Schemas para PreferenciasUsuario (por dispositivo).
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, time
from app.schemas.base import NivelExperienciaEnum, TemaEnum


class PreferenciasUsuarioResponse(BaseModel):
    """Respuesta de preferencias del usuario."""
    id: UUID
    dispositivo_id: UUID
    idioma_id: UUID | None = None
    notificaciones_habilitadas: bool
    frecuencia_recordatorio_minutos: int
    hora_inicio_trabajo: time | None = None
    hora_fin_trabajo: time | None = None
    nivel_experiencia: str
    objetivo_principal: str | None = None
    tema: str
    sonido_habilitado: bool
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


class PreferenciasUsuarioUpdateSchema(BaseModel):
    """Actualizar preferencias."""
    idioma_id: UUID | None = None
    notificaciones_habilitadas: bool | None = None
    frecuencia_recordatorio_minutos: int | None = Field(None, ge=5)
    hora_inicio_trabajo: time | None = None
    hora_fin_trabajo: time | None = None
    nivel_experiencia: NivelExperienciaEnum | None = None
    objetivo_principal: str | None = Field(None, max_length=255)
    tema: TemaEnum | None = None
    sonido_habilitado: bool | None = None