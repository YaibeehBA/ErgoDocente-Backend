"""
Repository para Ejercicio.
"""
from sqlalchemy import select
from app.models.ejercicios import Ejercicio
from app.repositories.base import BaseRepository


class EjercicioRepository(BaseRepository[Ejercicio]):
    """Repository especializado para Ejercicio."""

    async def obtener_por_slug(self, slug: str) -> Ejercicio | None:
        """Obtener ejercicio por slug (unique)."""
        stmt = select(Ejercicio).where(Ejercicio.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def listar_por_categoria(
        self,
        categoria_id,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar ejercicios de una categoria."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"categoria_id": categoria_id, "esta_publicado": True},
        )

    async def listar_por_parte_cuerpo(
        self,
        parte_cuerpo: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar ejercicios por parte del cuerpo."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"parte_cuerpo": parte_cuerpo, "esta_publicado": True},
        )