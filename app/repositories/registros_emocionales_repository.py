"""
Repository para RegistroEmocional.
"""
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy import select
from app.models.registros_emocionales import RegistroEmocional
from app.repositories.base import BaseRepository


class RegistroEmocionalRepository(BaseRepository[RegistroEmocional]):
    """Repository especializado para RegistroEmocional."""

    async def listar_por_dispositivo(
        self,
        dispositivo_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar registros emocionales de un dispositivo."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"dispositivo_id": dispositivo_id},
            order_by="registrado_en",
            order_direction="desc",
        )

    async def listar_ultimas_horas(
        self,
        dispositivo_id: UUID,
        horas: int = 24,
    ) -> list[RegistroEmocional]:
        """Listar registros emocionales de las ultimas N horas."""
        desde = datetime.utcnow() - timedelta(hours=horas)
        stmt = select(RegistroEmocional).where(
            RegistroEmocional.dispositivo_id == dispositivo_id,
            RegistroEmocional.registrado_en >= desde,
        ).order_by(RegistroEmocional.registrado_en.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def contar_por_emocion_dispositivo(
        self,
        dispositivo_id: UUID,
        emocion_id: UUID,
    ) -> int:
        """Contar cuantas veces se registro una emocion por dispositivo."""
        stmt = select(RegistroEmocional).where(
            RegistroEmocional.dispositivo_id == dispositivo_id,
            RegistroEmocional.emocion_id == emocion_id,
        )
        result = await self.db.execute(stmt)
        return len(result.scalars().all())