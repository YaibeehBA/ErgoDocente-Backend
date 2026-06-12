"""
Logica de negocio para Ejercicio.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.ejercicios_repository import EjercicioRepository
from app.core.exceptions import ConflictoError
from app.services.base import BaseService


class EjercicioService(BaseService):
    """Service para gestion de ejercicios."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.ejercicios import Ejercicio
        self.repo = EjercicioRepository(db, Ejercicio)

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar ejercicios publicados paginados."""
        return await self.repo.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"esta_publicado": True},
        )

    async def listar_por_categoria(self, categoria_id: UUID, page: int = 1, page_size: int = 20):
        """Listar ejercicios de una categoria."""
        return await self.repo.listar_por_categoria(categoria_id, page, page_size)

    async def listar_por_parte_cuerpo(self, parte_cuerpo: str, page: int = 1, page_size: int = 20):
        """Listar ejercicios por parte del cuerpo."""
        return await self.repo.listar_por_parte_cuerpo(parte_cuerpo, page, page_size)

    async def obtener_por_slug(self, slug: str):
        """Obtener ejercicio por slug."""
        return await self.repo.obtener_por_slug(slug)

    async def obtener_por_id(self, id: UUID):
        """Obtener ejercicio por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, datos: dict):
        """Crear ejercicio."""
        existente = await self.repo.obtener_por_slug(datos.get("slug", ""))
        if existente:
            raise ConflictoError(f"Ejercicio con slug '{datos['slug']}' ya existe", "slug")
        ejercicio = await self.repo.crear(datos)
        await self.commit()
        self.logger.info("ejercicio_creado", slug=datos.get("slug"))
        return ejercicio

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar ejercicio."""
        ejercicio = await self.repo.actualizar(id, datos)
        await self.commit()
        return ejercicio

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de ejercicio."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()