"""
Repository para RecomendacionEmocional.
"""
from uuid import UUID
from sqlalchemy import select
from app.models.recomendaciones_emocionales import RecomendacionEmocional
from app.repositories.base import BaseRepository


class RecomendacionEmocionalRepository(BaseRepository[RecomendacionEmocional]):
    """Repository especializado para RecomendacionEmocional."""

    async def listar_por_emocion(
        self,
        emocion_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar recomendaciones para una emocion especifica."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"emocion_id": emocion_id},
            order_by="prioridad",
            order_direction="asc",
        )

    async def obtener_recomendaciones_emocion(
        self,
        emocion_id: UUID,
    ) -> list[RecomendacionEmocional]:
        """Obtener todas las recomendaciones de una emocion ordenadas por prioridad."""
        stmt = select(RecomendacionEmocional).where(
            RecomendacionEmocional.emocion_id == emocion_id
        ).order_by(RecomendacionEmocional.prioridad)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())