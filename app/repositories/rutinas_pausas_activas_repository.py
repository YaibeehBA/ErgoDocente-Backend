"""
Repository para RutinaPausaActiva.
"""
from sqlalchemy import select
from app.models.rutinas_pausas_activas import RutinaPausaActiva
from app.repositories.base import BaseRepository


class RutinaPausaActivaRepository(BaseRepository[RutinaPausaActiva]):
    """Repository especializado para RutinaPausaActiva."""

    async def obtener_por_slug(self, slug: str) -> RutinaPausaActiva | None:
        """Obtener rutina por slug (unique)."""
        stmt = select(RutinaPausaActiva).where(RutinaPausaActiva.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def listar_recomendadas(self, page: int = 1, page_size: int = 20) -> tuple[list, int]:
        """Listar rutinas predeterminadas/recomendadas."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"esta_publicado": True, "es_predeterminado": True},
        )

    async def listar_destacadas(self, page: int = 1, page_size: int = 20) -> tuple[list, int]:
        """Listar rutinas destacadas."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"esta_publicado": True, "esta_destacado": True},
        )