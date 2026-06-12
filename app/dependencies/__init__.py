"""
Funciones de inyeccion de dependencias para routers.
"""
from typing import AsyncGenerator
from fastapi import Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import sanitizar_device_id


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency para inyectar sesion de BD en routers."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_device_id(x_device_id: str = Header(None)) -> str:
    """
    Dependency para extraer y validar device_id del header X-Device-ID.
    V1: El device_id identifica al usuario (sin JWT).
    """
    if not x_device_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header X-Device-ID es requerido",
        )
    
    try:
        return sanitizar_device_id(x_device_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"X-Device-ID invalido: {str(e)}",
        )


async def get_device_id_optional(x_device_id: str | None = Header(None)) -> str | None:
    """Dependency opcional para device_id."""
    if not x_device_id:
        return None
    
    try:
        return sanitizar_device_id(x_device_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"X-Device-ID invalido: {str(e)}",
        )