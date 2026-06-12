"""
Logica de negocio para EjercicioRutina (pivote N:N).
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.ejercicios_rutina_repository import EjercicioRutinaRepository
from app.core.exceptions import ConflictoError
from app.services.base import BaseService


class EjercicioRutinaService(BaseService):
    """Service para gestion de ejercicios dentro de rutinas."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.ejercicios_rutina import EjercicioRutina
        self.repo = EjercicioRutinaRepository(db, EjercicioRutina)

    async def listar_por_rutina(self, rutina_id: UUID, page: int = 1, page_size: int = 50):
        """Listar ejercicios de una rutina ordenados."""
        return await self.repo.listar_por_rutina(rutina_id, page, page_size)

    async def agregar_ejercicio(self, rutina_id: UUID, ejercicio_id: UUID, datos: dict):
        """Agregar ejercicio a una rutina."""
        existente = await self.repo.obtener_por_rutina_ejercicio(rutina_id, ejercicio_id)
        if existente:
            raise ConflictoError(f"EjercicioRutina con rutina_id '{rutina_id}' y ejercicio_id '{ejercicio_id}' ya existe", "rutina_id+ejercicio_id")
        datos["rutina_id"] = rutina_id
        datos["ejercicio_id"] = ejercicio_id
        entrada = await self.repo.crear(datos)
        await self.commit()
        return entrada

    async def actualizar_ejercicio(self, rutina_id: UUID, ejercicio_id: UUID, datos: dict):
        """Actualizar datos de un ejercicio en una rutina."""
        entrada = await self.repo.obtener_por_rutina_ejercicio(rutina_id, ejercicio_id)
        if not entrada:
            from app.core.exceptions import RecursoNoEncontradoError
            raise RecursoNoEncontradoError(f"EjercicioRutina con rutina_id '{rutina_id}' y ejercicio_id '{ejercicio_id}' no encontrado", "rutina_id+ejercicio_id")
        actualizado = await self.repo.actualizar(entrada.id, datos)
        await self.commit()
        return actualizado

    async def eliminar_ejercicio(self, rutina_id: UUID, ejercicio_id: UUID) -> None:
        """Eliminar ejercicio de una rutina."""
        entrada = await self.repo.obtener_por_rutina_ejercicio(rutina_id, ejercicio_id)
        if not entrada:
            from app.core.exceptions import RecursoNoEncontradoError
            raise RecursoNoEncontradoError(f"EjercicioRutina con rutina_id '{rutina_id}' y ejercicio_id '{ejercicio_id}' no encontrado", "rutina_id+ejercicio_id")
        await self.repo.eliminar(entrada.id, soft=False)
        await self.commit()