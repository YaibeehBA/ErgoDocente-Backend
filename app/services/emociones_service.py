"""
Logica de negocio para Emocion.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.emociones_repository import EmocionRepository
from app.core.exceptions import ConflictoError, RecursoNoEncontradoError
from app.services.base import BaseService


class EmocionService(BaseService):
    """Service para catalogo de emociones."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.emociones import Emocion
        self.repo = EmocionRepository(db, Emocion)

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar emociones activas."""
        return await self.repo.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"esta_activo": True},
        )

    async def listar_positivas(self, page: int = 1, page_size: int = 20):
        """Listar emociones positivas."""
        return await self.repo.listar_positivas(page, page_size)

    async def listar_negativas(self, page: int = 1, page_size: int = 20):
        """Listar emociones negativas/neutrales."""
        return await self.repo.listar_negativas(page, page_size)

    async def obtener_por_slug(self, slug: str):
        """Obtener emocion por slug."""
        emocion = await self.repo.obtener_por_slug(slug)
        if not emocion:
            raise RecursoNoEncontradoError("Emocion", slug)
        return emocion

    async def obtener_por_id(self, id: UUID):
        """Obtener emocion por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, datos: dict):
        """Crear emocion."""
        existente = await self.repo.obtener_por_slug(datos.get("slug", ""))
        if existente:
            raise ConflictoError(f"Emocion con slug '{datos['slug']}' ya existe", "slug")
        emocion = await self.repo.crear(datos)
        await self.commit()
        return emocion

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar emocion."""
        emocion = await self.repo.actualizar(id, datos)
        await self.commit()
        return emocion