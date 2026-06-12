"""
Repository para Idioma.
"""
from sqlalchemy import select
from app.models.idiomas import Idioma
from app.repositories.base import BaseRepository


class IdiomaRepository(BaseRepository[Idioma]):
    """Repository especializado para Idioma."""

    async def obtener_por_codigo(self, codigo: str) -> Idioma | None:
        """Obtener idioma por codigo (unique): es, kw"""
        stmt = select(Idioma).where(Idioma.codigo == codigo)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def obtener_predeterminado(self) -> Idioma | None:
        """Obtener idioma predeterminado (espanol)."""
        stmt = select(Idioma).where(Idioma.es_predeterminado == True)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()