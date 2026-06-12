"""
Schemas para ArchivoMedia (Cloudinary).
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.schemas.base import TipoRecursoEnum


class ArchivoMediaUploadSchema(BaseModel):
    """Parámetros para subir archivo."""
    tipo_recurso: TipoRecursoEnum
    nombre_original: str | None = Field(None, max_length=255)
    descripcion: str | None = Field(None, max_length=500)
    texto_alternativo: str | None = Field(None, max_length=500)


class ArchivoMediaResponse(BaseModel):
    """Respuesta de archivo media."""
    id: UUID
    public_id_cloudinary: str
    url_publica: str
    url_segura: str
    tipo_recurso: str
    formato: str | None = None
    tamano_bytes: int | None = None
    ancho_px: int | None = None
    alto_px: int | None = None
    duracion_segundos: float | None = None
    nombre_original: str | None = None
    descripcion: str | None = None
    texto_alternativo: str | None = None
    esta_activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True


class ArchivosMediaListResponse(BaseModel):
    """Respuesta paginada de archivos."""
    items: list[ArchivoMediaResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool