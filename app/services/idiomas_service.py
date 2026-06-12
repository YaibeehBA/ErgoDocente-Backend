"""
Logica de negocio para Idioma.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.idiomas_repository import IdiomaRepository
from app.core.exceptions import RecursoNoEncontradoError
from app.services.base import BaseService


class IdiomaService(BaseService):
    """Service para gestion de idiomas."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.idiomas import Idioma
        self.repo = IdiomaRepository(db, Idioma)

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar idiomas disponibles."""
        return await self.repo.listar_paginado(page=page, page_size=page_size)

    async def obtener_por_codigo(self, codigo: str):
        """Obtener idioma por codigo (es, kw)."""
        idioma = await self.repo.obtener_por_codigo(codigo)
        if not idioma:
            raise RecursoNoEncontradoError("Idioma", codigo)
        return idioma

    async def obtener_predeterminado(self):
        """Obtener idioma predeterminado (espanol)."""
        return await self.repo.obtener_predeterminado()