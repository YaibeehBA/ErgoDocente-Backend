"""
Schemas para RegistroAuditoria (admin only).
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class RegistroAuditoriaResponse(BaseModel):
    """Respuesta de registro de auditoría."""
    id: UUID
    accion: str
    tabla_afectada: str
    registro_id: str
    usuario_id: str | None
    dispositivo_id: str | None
    direccion_ip: str | None
    razon_cambio: str | None
    endpoint_api: str | None
    ocurrido_en: datetime

    class Config:
        from_attributes = True


class RegistrosAuditoriaListResponse(BaseModel):
    """Respuesta paginada."""
    items: list[RegistroAuditoriaResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool