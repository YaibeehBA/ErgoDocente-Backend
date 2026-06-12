"""
Repository para Dispositivo.
device_id es UNIQUE y critico para V1 (auth sin JWT).
"""
from sqlalchemy import select
from app.models.dispositivos import Dispositivo
from app.models.preferencias_usuario import PreferenciasUsuario
from app.repositories.base import BaseRepository


class DispositivoRepository(BaseRepository[Dispositivo]):
    """Repository especializado para Dispositivo."""

    async def obtener_por_device_id(self, device_id: str) -> Dispositivo | None:
        """Obtener dispositivo por identificador_dispositivo (unique)."""
        stmt = select(Dispositivo).where(
            Dispositivo.identificador_dispositivo == device_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def registrar_dispositivo(self, dispositivo_in: dict) -> Dispositivo:
        """
        Registrar nuevo dispositivo y crear preferencias por defecto.
        Automaticamente crea PreferenciasUsuario asociadas.
        """
        dispositivo = await self.crear(dispositivo_in)
        prefs = PreferenciasUsuario(
            dispositivo_id=dispositivo.id,
            idioma_id=None,
        )
        self.db.add(prefs)
        await self.db.flush()
        return dispositivo