"""
Repository para EjercicioRutina (pivote N:N con datos extra).
"""
from uuid import UUID
from sqlalchemy import select
from app.models.ejercicios_rutina import EjercicioRutina
from app.repositories.base import BaseRepository


class EjercicioRutinaRepository(BaseRepository[EjercicioRutina]):
    """Repository especializado para EjercicioRutina."""

    async def obtener_por_rutina_ejercicio(
        self,
        rutina_id: UUID,
        ejercicio_id: UUID,
    ) -> EjercicioRutina | None:
        """Obtener entrada especifica de ejercicio en rutina."""
        stmt = select(EjercicioRutina).where(
            EjercicioRutina.rutina_id == rutina_id,
            EjercicioRutina.ejercicio_id == ejercicio_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def listar_por_rutina(
        self,
        rutina_id: UUID,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list, int]:
        """Listar ejercicios de una rutina ordenados por orden."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"rutina_id": rutina_id},
            order_by="orden",
            order_direction="asc",
        )