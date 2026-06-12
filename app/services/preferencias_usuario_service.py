"""
Logica de negocio para PreferenciasUsuario.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.preferencias_usuario_repository import PreferenciasUsuarioRepository
from app.core.exceptions import RecursoNoEncontradoError
from app.services.base import BaseService


class PreferenciasUsuarioService(BaseService):
    """Service para preferencias de usuario por dispositivo."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.preferencias_usuario import PreferenciasUsuario
        self.repo = PreferenciasUsuarioRepository(db, PreferenciasUsuario)

    async def obtener_por_dispositivo(self, dispositivo_id: UUID):
        """Obtener preferencias del dispositivo."""
        prefs = await self.repo.obtener_por_dispositivo(dispositivo_id)
        if not prefs:
            raise RecursoNoEncontradoError("PreferenciasUsuario", dispositivo_id)
        return prefs

    async def actualizar(self, dispositivo_id: UUID, datos: dict):
        """Actualizar preferencias del dispositivo."""
        prefs = await self.obtener_por_dispositivo(dispositivo_id)
        actualizado = await self.repo.actualizar(prefs.id, datos)
        await self.commit()
        return actualizado