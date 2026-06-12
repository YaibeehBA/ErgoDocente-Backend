"""
Logica de negocio para RegistroAuditoria (solo lectura, admin).
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.registros_auditoria_repository import RegistroAuditoriaRepository
from app.services.base import BaseService


class RegistroAuditoriaService(BaseService):
    """Service para consulta de auditoria (admin only, solo lectura)."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.registros_auditoria import RegistroAuditoria
        self.repo = RegistroAuditoriaRepository(db, RegistroAuditoria)

    async def listar_por_tabla(self, tabla: str, page: int = 1, page_size: int = 20):
        """Listar auditoria de una tabla."""
        return await self.repo.listar_por_tabla(tabla, page, page_size)

    async def listar_por_registro(self, tabla: str, registro_id: str, page: int = 1, page_size: int = 20):
        """Listar cambios de un registro especifico."""
        return await self.repo.listar_por_registro(tabla, registro_id, page, page_size)

    async def listar_por_dispositivo(self, dispositivo_id: str, page: int = 1, page_size: int = 20):
        """Listar acciones realizadas por un dispositivo."""
        return await self.repo.listar_por_dispositivo(dispositivo_id, page, page_size)