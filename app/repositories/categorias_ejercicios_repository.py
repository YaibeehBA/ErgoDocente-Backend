"""
Repository para CategoriaEjercicio.
"""
from sqlalchemy import select
from app.models.categorias_ejercicios import CategoriaEjercicio
from app.repositories.base import BaseRepository


class CategoriaEjercicioRepository(BaseRepository[CategoriaEjercicio]):
    """Repository especializado para CategoriaEjercicio."""

    async def obtener_por_slug(self, slug: str) -> CategoriaEjercicio | None:
        """Obtener categoria por slug (unique)."""
        stmt = select(CategoriaEjercicio).where(CategoriaEjercicio.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()