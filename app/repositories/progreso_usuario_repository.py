"""
Repository para ProgresoUsuario. Incluye logica de gamificacion basica.
"""
from uuid import UUID
from sqlalchemy import select
from app.models.progreso_usuario import ProgresoUsuario
from app.repositories.base import BaseRepository


class ProgresoUsuarioRepository(BaseRepository[ProgresoUsuario]):
    """Repository especializado para ProgresoUsuario."""

    async def registrar_actividad(
        self,
        dispositivo_id: UUID,
        tipo_actividad: str,
        referencia_id: UUID,
        tipo_referencia: str,
        duracion_real_segundos: int | None = None,
        completado: bool = True,
        porcentaje_completado: int = 100,
    ) -> ProgresoUsuario:
        """Registrar actividad completada por usuario."""
        puntos = 10 if completado else int(10 * porcentaje_completado / 100)
        return await self.crear({
            "dispositivo_id": dispositivo_id,
            "tipo_actividad": tipo_actividad,
            "referencia_id": referencia_id,
            "tipo_referencia": tipo_referencia,
            "duracion_real_segundos": duracion_real_segundos,
            "completado": completado,
            "porcentaje_completado": porcentaje_completado,
            "puntos_ganados": puntos,
        })

    async def listar_por_dispositivo(
        self,
        dispositivo_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar progreso de un dispositivo."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"dispositivo_id": dispositivo_id},
            order_by="realizado_en",
            order_direction="desc",
        )

    async def contar_puntos_dispositivo(self, dispositivo_id: UUID) -> int:
        """Contar puntos totales de un dispositivo."""
        stmt = select(ProgresoUsuario.puntos_ganados.sum()).where(
            ProgresoUsuario.dispositivo_id == dispositivo_id,
            ProgresoUsuario.completado == True,
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0