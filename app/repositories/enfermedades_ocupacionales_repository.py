"""
Repository para EnfermedadOcupacional.
"""
from sqlalchemy import select
from app.models.enfermedades_ocupacionales import EnfermedadOcupacional
from app.repositories.base import BaseRepository


class EnfermedadOcupacionalRepository(BaseRepository[EnfermedadOcupacional]):
    """Repository especializado para EnfermedadOcupacional."""

    async def obtener_por_slug(self, slug: str) -> EnfermedadOcupacional | None:
        """Obtener enfermedad por slug (unique)."""
        stmt = select(EnfermedadOcupacional).where(EnfermedadOcupacional.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()