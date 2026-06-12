"""
Logica de negocio para Consejo.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.consejos_repository import ConsejoRepository
from app.core.exceptions import ConflictoError
from app.services.base import BaseService


class ConsejoService(BaseService):
    """Service para gestion de consejos de salud."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.consejos import Consejo
        self.repo = ConsejoRepository(db, Consejo)

    async def listar_publicados(self, page: int = 1, page_size: int = 20):
        """Listar consejos publicados."""
        return await self.repo.listar_publicados(page, page_size)

    async def listar_por_categoria(self, categoria: str, page: int = 1, page_size: int = 20):
        """Listar consejos por categoria."""
        return await self.repo.listar_por_categoria(categoria, page, page_size)

    async def obtener_por_slug(self, slug: str):
        """Obtener consejo por slug."""
        return await self.repo.obtener_por_slug(slug)

    async def obtener_por_id(self, id: UUID):
        """Obtener consejo por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, datos: dict):
        """Crear consejo."""
        existente = await self.repo.obtener_por_slug(datos.get("slug", ""))
        if existente:
            raise ConflictoError(f"Consejo con slug '{datos['slug']}' ya existe", "slug")
        consejo = await self.repo.crear(datos)
        await self.commit()
        return consejo

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar consejo."""
        consejo = await self.repo.actualizar(id, datos)
        await self.commit()
        return consejo

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de consejo."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()