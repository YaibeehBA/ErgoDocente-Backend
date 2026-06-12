"""
device_id es el identificador principal en V1.
"""
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from app.schemas.base import PlataformaEnum


class DispositivoRegisterSchema(BaseModel):
    """
    Registrar un nuevo dispositivo.
    Se ejecuta la primera vez que la app se instala.
    """
    identificador_dispositivo: str = Field(
        ...,
        min_length=8,
        max_length=255,
        description="UUID generado por la app móvil"
    )
    plataforma: PlataformaEnum
    modelo_dispositivo: str | None = Field(None, max_length=100)
    version_so: str | None = Field(None, max_length=50)
    version_app: str | None = Field(None, max_length=20)
    token_notificacion: str | None = Field(None, description="FCM/APNs token")

    @field_validator('identificador_dispositivo', mode='before')
    @classmethod
    def validar_device_id(cls, v: str) -> str:
        """Sanitizar device_id."""
        from app.core.security import sanitizar_device_id
        try:
            return sanitizar_device_id(v)
        except ValueError as e:
            raise ValueError(f"device_id inválido: {str(e)}")


class DispositivoUpdateSchema(BaseModel):
    """Actualizar datos del dispositivo."""
    nombre_dispositivo: str | None = Field(None, max_length=255)
    token_notificacion: str | None = None
    version_app: str | None = Field(None, max_length=20)


class DispositivoResponse(BaseModel):
    """Respuesta al registrar/consultar dispositivo."""
    id: UUID
    identificador_dispositivo: str
    nombre_dispositivo: str | None = None
    plataforma: str | None = None
    modelo_dispositivo: str | None = None
    version_so: str | None = None
    version_app: str | None = None
    esta_activo: bool
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


class DispositivosListResponse(BaseModel):
    """Respuesta paginada de dispositivos."""
    items: list[DispositivoResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool