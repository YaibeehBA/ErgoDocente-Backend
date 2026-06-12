"""
Logica de negocio para ContenidoErgonomico.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.contenidos_ergonomicos_repository import ContenidoErgonomicoRepository
from app.core.exceptions import ConflictoError
from app.services.base import BaseService


class ContenidoErgonomicoService(BaseService):
    """Service para contenidos ergonomicos educativos."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.contenidos_ergonomicos import ContenidoErgonomico
        self.repo = ContenidoErgonomicoRepository(db, ContenidoErgonomico)

    async def listar_publicados(self, page: int = 1, page_size: int = 20):
        """Listar contenidos publicados."""
        return await self.repo.listar_publicados(page=page, page_size=page_size)

    async def obtener_por_slug(self, slug: str):
        """Obtener contenido por slug."""
        return await self.repo.obtener_por_slug(slug)

    async def obtener_por_id(self, id: UUID):
        """Obtener contenido por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, datos: dict):
        """Crear contenido ergonomico."""
        existente = await self.repo.obtener_por_slug(datos.get("slug", ""))
        if existente:
            raise ConflictoError(f"ContenidoErgonomico con slug '{datos['slug']}' ya existe", "slug")
        contenido = await self.repo.crear(datos)
        await self.commit()
        return contenido

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar contenido ergonomico."""
        contenido = await self.repo.actualizar(id, datos)
        await self.commit()
        return contenido

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de contenido."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar todos los contenidos paginados."""
        return await self.repo.listar_paginado(page=page, page_size=page_size)