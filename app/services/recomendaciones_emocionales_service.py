"""
Logica de negocio para RecomendacionEmocional.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.recomendaciones_emocionales_repository import RecomendacionEmocionalRepository
from app.services.base import BaseService


class RecomendacionEmocionalService(BaseService):
    """Service para recomendaciones basadas en emociones."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.recomendaciones_emocionales import RecomendacionEmocional
        self.repo = RecomendacionEmocionalRepository(db, RecomendacionEmocional)

    async def listar_por_emocion(self, emocion_id: UUID, page: int = 1, page_size: int = 20):
        """Listar recomendaciones para una emocion."""
        return await self.repo.listar_por_emocion(emocion_id, page, page_size)

    async def obtener_para_emocion(self, emocion_id: UUID) -> list:
        """Obtener todas las recomendaciones de una emocion ordenadas por prioridad."""
        return list(await self.repo.obtener_recomendaciones_emocion(emocion_id))

    async def obtener_por_id(self, id: UUID):
        """Obtener recomendacion por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, datos: dict):
        """Crear recomendacion emocional."""
        recomendacion = await self.repo.crear(datos)
        await self.commit()
        return recomendacion

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar recomendacion."""
        recomendacion = await self.repo.actualizar(id, datos)
        await self.commit()
        return recomendacion

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de recomendacion."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()