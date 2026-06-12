"""
Repository para Consejo.
"""
from sqlalchemy import select
from app.models.consejos import Consejo
from app.repositories.base import BaseRepository


class ConsejoRepository(BaseRepository[Consejo]):
    """Repository especializado para Consejo."""

    async def obtener_por_slug(self, slug: str) -> Consejo | None:
        """Obtener consejo por slug (unique)."""
        stmt = select(Consejo).where(Consejo.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def listar_por_categoria(
        self,
        categoria: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar consejos por categoria publicados."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"categoria": categoria, "esta_publicado": True},
            order_by="orden",
        )

    async def listar_publicados(self, page: int = 1, page_size: int = 20) -> tuple[list, int]:
        """Listar todos los consejos publicados."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"esta_publicado": True},
            order_by="orden",
        )