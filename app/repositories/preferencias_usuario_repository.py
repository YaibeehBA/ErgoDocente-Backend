"""
Repository para PreferenciasUsuario.
"""
from uuid import UUID
from sqlalchemy import select
from app.models.preferencias_usuario import PreferenciasUsuario
from app.repositories.base import BaseRepository


class PreferenciasUsuarioRepository(BaseRepository[PreferenciasUsuario]):
    """Repository especializado para PreferenciasUsuario."""

    async def obtener_por_dispositivo(self, dispositivo_id: UUID) -> PreferenciasUsuario | None:
        """Obtener preferencias por dispositivo (unique)."""
        stmt = select(PreferenciasUsuario).where(
            PreferenciasUsuario.dispositivo_id == dispositivo_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()