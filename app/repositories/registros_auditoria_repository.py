"""
Repository para RegistroAuditoria (admin only).
"""
from app.models.registros_auditoria import RegistroAuditoria
from app.repositories.base import BaseRepository


class RegistroAuditoriaRepository(BaseRepository[RegistroAuditoria]):
    """Repository especializado para RegistroAuditoria."""

    async def listar_por_tabla(
        self,
        tabla: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar registros de auditoria de una tabla."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"tabla_afectada": tabla},
            order_by="ocurrido_en",
            order_direction="desc",
            incluir_eliminados=True,
        )

    async def listar_por_registro(
        self,
        tabla: str,
        registro_id: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar cambios de un registro especifico."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"tabla_afectada": tabla, "registro_id": registro_id},
            order_by="ocurrido_en",
            order_direction="desc",
            incluir_eliminados=True,
        )

    async def listar_por_dispositivo(
        self,
        dispositivo_id: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar auditoria de cambios hechos por un dispositivo."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"dispositivo_id": dispositivo_id},
            order_by="ocurrido_en",
            order_direction="desc",
            incluir_eliminados=True,
        )