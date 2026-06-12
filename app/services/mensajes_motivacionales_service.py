"""
Logica de negocio para MensajeMotivacional.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.mensajes_motivacionales_repository import MensajeMotivacionalRepository
from app.services.base import BaseService


class MensajeMotivacionalService(BaseService):
    """Service para mensajes motivacionales."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.mensajes_motivacionales import MensajeMotivacional
        self.repo = MensajeMotivacionalRepository(db, MensajeMotivacional)

    async def listar_publicados(self, page: int = 1, page_size: int = 20):
        """Listar mensajes publicados."""
        return await self.repo.listar_publicados(page, page_size)

    async def listar_por_categoria(self, categoria: str, page: int = 1, page_size: int = 20):
        """Listar mensajes por categoria."""
        return await self.repo.listar_por_categoria(categoria, page, page_size)

    async def obtener_aleatorio(self):
        """Obtener mensaje motivacional aleatorio."""
        return await self.repo.obtener_aleatorio()

    async def obtener_por_id(self, id: UUID):
        """Obtener mensaje por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, datos: dict):
        """Crear mensaje motivacional."""
        mensaje = await self.repo.crear(datos)
        await self.commit()
        return mensaje

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar mensaje."""
        mensaje = await self.repo.actualizar(id, datos)
        await self.commit()
        return mensaje

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de mensaje."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()