"""
Repository para ContenidoErgonomico.
"""
from sqlalchemy import select
from app.models.contenidos_ergonomicos import ContenidoErgonomico
from app.repositories.base import BaseRepository


class ContenidoErgonomicoRepository(BaseRepository[ContenidoErgonomico]):
    """Repository especializado para ContenidoErgonomico."""

    async def obtener_por_slug(self, slug: str) -> ContenidoErgonomico | None:
        """Obtener contenido por slug (unique)."""
        stmt = select(ContenidoErgonomico).where(ContenidoErgonomico.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def listar_publicados(self, page: int = 1, page_size: int = 20) -> tuple[list, int]:
        """Listar solo contenidos publicados."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"esta_publicado": True},
        )