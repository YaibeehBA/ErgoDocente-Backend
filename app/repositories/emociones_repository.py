"""
Repository para Emocion.
"""
from sqlalchemy import select
from app.models.emociones import Emocion
from app.repositories.base import BaseRepository


class EmocionRepository(BaseRepository[Emocion]):
    """Repository especializado para Emocion."""

    async def obtener_por_slug(self, slug: str) -> Emocion | None:
        """Obtener emocion por slug (unique)."""
        stmt = select(Emocion).where(Emocion.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def listar_positivas(self, page: int = 1, page_size: int = 20) -> tuple[list, int]:
        """Listar emociones positivas activas."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"es_positiva": True, "esta_activo": True},
        )

    async def listar_negativas(self, page: int = 1, page_size: int = 20) -> tuple[list, int]:
        """Listar emociones negativas activas."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"es_positiva": False, "esta_activo": True},
        )