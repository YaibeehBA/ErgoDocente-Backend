"""
Logica de negocio para Usuario.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.usuarios_repository import UsuarioRepository
from app.core.exceptions import RecursoNoEncontradoError, ConflictoError
from app.core.security import hashear_password
from app.services.base import BaseService
from app.models.usuarios import Usuario


class UsuarioService(BaseService):
    """Service para gestion de usuarios."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.repo = UsuarioRepository(db, model=Usuario)

    async def obtener_por_id(self, id: UUID):
        """Obtener usuario por ID."""
        return await self.repo.obtener_o_error(id)

    async def obtener_por_correo(self, correo: str):
        """Obtener usuario por correo."""
        usuario = await self.repo.obtener_por_correo(correo)
        if not usuario:
            raise RecursoNoEncontradoError(f"Usuario con correo '{correo}' no encontrado", correo)
        return usuario

    async def crear(self, datos: dict):
        """Crear usuario con password hasheado."""
        existente = await self.repo.obtener_por_correo(datos.get("correo", ""))
        if existente:
            raise ConflictoError(f"Usuario con correo '{datos['correo']}' ya existe", "correo")

        if "password" in datos:
            datos["password_hash"] = hashear_password(datos.pop("password"))

        usuario = await self.repo.crear(datos)
        await self.commit()
        self.logger.info("usuario_creado", usuario_id=str(usuario.id))
        return usuario

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar usuario."""
        usuario = await self.repo.actualizar(id, datos)
        await self.commit()
        return usuario

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de usuario."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar usuarios paginados."""
        return await self.repo.listar_paginado(page=page, page_size=page_size)