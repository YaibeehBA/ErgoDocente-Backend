"""
Repository para Usuario.
"""
from sqlalchemy import select
from app.models.usuarios import Usuario
from app.repositories.base import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    """Repository especializado para Usuario."""

    async def obtener_por_correo(self, correo: str) -> Usuario | None:
        """Obtener usuario por correo (unique)."""
        stmt = select(Usuario).where(Usuario.correo == correo)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Usuario | None:
        """Obtener usuario por nombre_usuario (unique)."""
        stmt = select(Usuario).where(Usuario.nombre_usuario == nombre_usuario)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()