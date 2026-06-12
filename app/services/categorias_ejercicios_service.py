"""
Logica de negocio para CategoriaEjercicio.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.categorias_ejercicios_repository import CategoriaEjercicioRepository
from app.core.exceptions import ConflictoError
from app.services.base import BaseService


class CategoriaEjercicioService(BaseService):
    """Service para categorias de ejercicios."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.categorias_ejercicios import CategoriaEjercicio
        self.repo = CategoriaEjercicioRepository(db, CategoriaEjercicio)

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar categorias paginadas."""
        return await self.repo.listar_paginado(page=page, page_size=page_size)

    async def obtener_por_slug(self, slug: str):
        """Obtener categoria por slug."""
        return await self.repo.obtener_por_slug(slug)

    async def obtener_por_id(self, id: UUID):
        """Obtener categoria por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, datos: dict):
        """Crear categoria de ejercicio."""
        existente = await self.repo.obtener_por_slug(datos.get("slug", ""))
        if existente:
            raise ConflictoError(f"CategoriaEjercicio con slug '{datos['slug']}' ya existe", "slug")
        categoria = await self.repo.crear(datos)
        await self.commit()
        return categoria

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar categoria."""
        categoria = await self.repo.actualizar(id, datos)
        await self.commit()
        return categoria

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de categoria."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()