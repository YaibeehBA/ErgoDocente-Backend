"""
Repository para Recordatorio.
"""
from uuid import UUID
from sqlalchemy import select
from app.models.recordatorios import Recordatorio
from app.repositories.base import BaseRepository


class RecordatorioRepository(BaseRepository[Recordatorio]):
    """Repository especializado para Recordatorio."""

    async def listar_por_dispositivo(
        self,
        dispositivo_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar recordatorios de un dispositivo."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"dispositivo_id": dispositivo_id},
            incluir_eliminados=False,
        )

    async def listar_activos_dispositivo(self, dispositivo_id: UUID) -> list[Recordatorio]:
        """Listar recordatorios activos de un dispositivo."""
        stmt = select(Recordatorio).where(
            Recordatorio.dispositivo_id == dispositivo_id,
            Recordatorio.esta_activo == True,
            Recordatorio.eliminado_en.is_(None),
        ).order_by(Recordatorio.hora)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())