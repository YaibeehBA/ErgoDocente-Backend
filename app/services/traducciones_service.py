"""
Logica de negocio para el sistema polimorfico de traducciones.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.traducciones_repository import TraduccionRepository
from app.services.base import BaseService


class TraduccionService(BaseService):
    """Service para gestion de traducciones polimorficas."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.traducciones import Traduccion
        self.repo = TraduccionRepository(db, Traduccion)

    async def obtener(
        self,
        tabla: str,
        registro_id: UUID,
        idioma_id: UUID | None = None,
    ) -> dict[str, str]:
        """Obtener todas las traducciones de un registro."""
        return await self.repo.obtener_traducciones(tabla, registro_id, idioma_id)

    async def obtener_campo(
        self,
        tabla: str,
        registro_id: UUID,
        campo: str,
        idioma_id: UUID | None = None,
    ) -> str | None:
        """Obtener traduccion de un campo especifico."""
        return await self.repo.obtener_traduccion_campo(tabla, registro_id, campo, idioma_id)

    async def crear(self, datos: dict):
        """Crear o actualizar una traduccion."""
        traduccion = await self.repo.crear(datos)
        await self.commit()
        return traduccion

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar traducciones paginadas."""
        return await self.repo.listar_paginado(page=page, page_size=page_size)