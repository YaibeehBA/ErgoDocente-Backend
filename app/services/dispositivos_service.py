"""
Logica de negocio para Dispositivo.
V1: El device_id identifica al usuario (sin JWT).
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dispositivos_repository import DispositivoRepository
from app.core.exceptions import RecursoNoEncontradoError
from app.services.base import BaseService


class DispositivoService(BaseService):
    """Service para gestion de dispositivos."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.dispositivos import Dispositivo
        self.repo = DispositivoRepository(db, Dispositivo)

    async def registrar(self, datos: dict):
        """Registrar dispositivo nuevo o retornar existente."""
        device_id = datos.get("identificador_dispositivo", "")
        existente = await self.repo.obtener_por_device_id(device_id)
        if existente:
            campos_actualizar = {k: v for k, v in datos.items()
                                if k not in ("identificador_dispositivo",) and v is not None}
            if campos_actualizar:
                actualizado = await self.repo.actualizar(existente.id, campos_actualizar)  
                await self.commit()
                self.logger.info("dispositivo_actualizado", device_id=device_id)
                return actualizado  
            return existente  # Si no hay cambios
        dispositivo = await self.repo.registrar_dispositivo(datos)
        await self.commit()
        self.logger.info("dispositivo_registrado", device_id=device_id)
        return dispositivo

    async def obtener_por_device_id(self, device_id: str):
        """Obtener dispositivo por device_id o lanzar excepcion."""
        dispositivo = await self.repo.obtener_por_device_id(device_id)
        if not dispositivo:
            raise RecursoNoEncontradoError("Dispositivo", device_id)
        return dispositivo

    async def obtener_por_id(self, id: UUID):
        """Obtener dispositivo por UUID."""
        return await self.repo.obtener_o_error(id)

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar dispositivos paginados."""
        return await self.repo.listar_paginado(page=page, page_size=page_size)