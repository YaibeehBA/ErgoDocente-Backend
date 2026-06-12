"""
Logica de negocio para ProgresoUsuario.
Incluye logica de gamificacion.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.progreso_usuario_repository import ProgresoUsuarioRepository
from app.services.base import BaseService


class ProgresoUsuarioService(BaseService):
    """Service para registro de progreso y gamificacion."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.progreso_usuario import ProgresoUsuario
        self.repo = ProgresoUsuarioRepository(db, ProgresoUsuario)

    async def registrar_actividad(
        self,
        dispositivo_id: UUID,
        tipo_actividad: str,
        referencia_id: UUID,
        tipo_referencia: str,
        duracion_real_segundos: int | None = None,
        completado: bool = True,
        porcentaje_completado: int = 100,
    ):
        """
        Registrar actividad completada.
        Calcula puntos automaticamente:
          - Completo: 10 puntos
          - Parcial: proporcional al porcentaje
        """
        progreso = await self.repo.registrar_actividad(
            dispositivo_id=dispositivo_id,
            tipo_actividad=tipo_actividad,
            referencia_id=referencia_id,
            tipo_referencia=tipo_referencia,
            duracion_real_segundos=duracion_real_segundos,
            completado=completado,
            porcentaje_completado=porcentaje_completado,
        )
        await self.commit()
        self.logger.info(
            "actividad_registrada",
            dispositivo_id=str(dispositivo_id),
            tipo=tipo_actividad,
            puntos=progreso.puntos_ganados,
        )
        return progreso

    async def listar_por_dispositivo(self, dispositivo_id: UUID, page: int = 1, page_size: int = 20):
        """Listar historial de progreso de un dispositivo."""
        return await self.repo.listar_por_dispositivo(dispositivo_id, page, page_size)

    async def obtener_puntos_totales(self, dispositivo_id: UUID) -> int:
        """Obtener puntos acumulados de un dispositivo."""
        return await self.repo.contar_puntos_dispositivo(dispositivo_id)

    async def obtener_nivel(self, dispositivo_id: UUID) -> dict:
        """
        Calcular nivel del usuario segun puntos acumulados.
        Niveles: Principiante (0-99), Intermedio (100-499),
                 Avanzado (500-999), Experto (1000+)
        """
        puntos = await self.obtener_puntos_totales(dispositivo_id)
        if puntos < 100:
            nivel = "principiante"
            siguiente = 100
        elif puntos < 500:
            nivel = "intermedio"
            siguiente = 500
        elif puntos < 1000:
            nivel = "avanzado"
            siguiente = 1000
        else:
            nivel = "experto"
            siguiente = None

        return {
            "puntos": puntos,
            "nivel": nivel,
            "puntos_para_siguiente_nivel": (siguiente - puntos) if siguiente else None,
        }