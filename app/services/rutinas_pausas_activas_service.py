"""
Logica de negocio para RutinaPausaActiva.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.rutinas_pausas_activas_repository import RutinaPausaActivaRepository
from app.core.exceptions import ConflictoError
from app.services.base import BaseService


class RutinaPausaActivaService(BaseService):
    """Service para rutinas de pausas activas."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.rutinas_pausas_activas import RutinaPausaActiva
        self.repo = RutinaPausaActivaRepository(db, RutinaPausaActiva)

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar rutinas publicadas paginadas."""
        return await self.repo.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"esta_publicado": True},
        )

    async def listar_recomendadas(self, page: int = 1, page_size: int = 20):
        """Listar rutinas recomendadas/predeterminadas."""
        return await self.repo.listar_recomendadas(page, page_size)

    async def listar_destacadas(self, page: int = 1, page_size: int = 20):
        """Listar rutinas destacadas."""
        return await self.repo.listar_destacadas(page, page_size)

    async def obtener_por_slug(self, slug: str):
        """Obtener rutina por slug."""
        return await self.repo.obtener_por_slug(slug)

    async def obtener_por_id(self, id: UUID):
        """Obtener rutina por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, datos: dict):
        """Crear rutina de pausa activa."""
        existente = await self.repo.obtener_por_slug(datos.get("slug", ""))
        if existente:
            raise ConflictoError(f"RutinaPausaActiva con slug '{datos['slug']}' ya existe", "slug")
        rutina = await self.repo.crear(datos)
        await self.commit()
        return rutina

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar rutina."""
        rutina = await self.repo.actualizar(id, datos)
        await self.commit()
        return rutina

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de rutina."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()