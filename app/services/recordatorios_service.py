"""
Logica de negocio para Recordatorio.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.recordatorios import Recordatorio
from app.repositories.recordatorios_repository import RecordatorioRepository
from app.services.base import BaseService


class RecordatorioService(BaseService):
    """Service para gestion de recordatorios por dispositivo."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.recordatorios import Recordatorio
        self.repo = RecordatorioRepository(db, Recordatorio)

    async def listar_por_dispositivo(self, dispositivo_id: UUID, page: int = 1, page_size: int = 20):
        """Listar recordatorios de un dispositivo."""
        return await self.repo.listar_por_dispositivo(dispositivo_id, page, page_size)

    async def listar_activos(self, dispositivo_id: UUID):
        """Listar solo recordatorios activos."""
        return await self.repo.listar_activos_dispositivo(dispositivo_id)

    async def obtener_por_id(self, id: UUID):
        """Obtener recordatorio por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, dispositivo_id: UUID, datos: dict):
        """Crear recordatorio para un dispositivo."""
        datos["dispositivo_id"] = dispositivo_id
        recordatorio = await self.repo.crear(datos)
        await self.commit()
        return recordatorio

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar recordatorio."""
        recordatorio = await self.repo.actualizar(id, datos)
        await self.commit()
        return recordatorio

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de recordatorio."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()

    async def toggle_activo(self, id: UUID) -> "Recordatorio":
        """Activar o desactivar un recordatorio."""
        recordatorio = await self.repo.obtener_o_error(id)
        nuevo_estado = not recordatorio.esta_activo
        actualizado = await self.repo.actualizar(id, {"esta_activo": nuevo_estado})
        await self.commit()
        return actualizado