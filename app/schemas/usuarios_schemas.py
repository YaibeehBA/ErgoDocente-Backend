"""
Schemas para la entidad Usuario.
V1: No se expone. V2: Se usará con autenticación JWT.
"""
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime
from app.schemas.base import RolEnum


class UsuarioBase(BaseModel):
    """Campos comunes entre Create y Update."""
    nombre_completo: str = Field(..., min_length=3, max_length=255)
    correo: EmailStr
    telefono: str | None = Field(None, max_length=20)


class UsuarioCreate(UsuarioBase):
    """Para POST /usuarios (V2 futuro)."""
    password: str = Field(..., min_length=8, description="Contraseña con validaciones")


class UsuarioUpdate(BaseModel):
    """Para PATCH /usuarios/{id}."""
    nombre_completo: str | None = Field(None, min_length=3, max_length=255)
    telefono: str | None = Field(None, max_length=20)


class UsuarioResponse(UsuarioBase):
    """Respuesta GET de usuario."""
    id: UUID
    nombre_usuario: str | None = None
    rol: str
    esta_activo: bool
    verificado_en: datetime | None = None
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


class UsuariosListResponse(BaseModel):
    """Respuesta paginada de usuarios."""
    items: list[UsuarioResponse]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool