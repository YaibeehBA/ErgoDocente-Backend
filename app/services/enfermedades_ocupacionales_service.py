"""
Logica de negocio para EnfermedadOcupacional.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.enfermedades_ocupacionales_repository import EnfermedadOcupacionalRepository
from app.core.exceptions import ConflictoError
from app.services.base import BaseService


class EnfermedadOcupacionalService(BaseService):
    """Service para catalogo de enfermedades ocupacionales."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.enfermedades_ocupacionales import EnfermedadOcupacional
        self.repo = EnfermedadOcupacionalRepository(db, EnfermedadOcupacional)

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar enfermedades paginadas."""
        return await self.repo.listar_paginado(page=page, page_size=page_size)

    async def obtener_por_slug(self, slug: str):
        """Obtener enfermedad por slug."""
        return await self.repo.obtener_por_slug(slug)

    async def obtener_por_id(self, id: UUID):
        """Obtener enfermedad por ID."""
        return await self.repo.obtener_o_error(id)

    async def crear(self, datos: dict):
        """Crear enfermedad ocupacional."""
        existente = await self.repo.obtener_por_slug(datos.get("slug", ""))
        if existente:
            raise ConflictoError(f"EnfermedadOcupacional con slug '{datos['slug']}' ya existe", "slug")
        enfermedad = await self.repo.crear(datos)
        await self.commit()
        return enfermedad

    async def actualizar(self, id: UUID, datos: dict):
        """Actualizar enfermedad ocupacional."""
        enfermedad = await self.repo.actualizar(id, datos)
        await self.commit()
        return enfermedad

    async def eliminar(self, id: UUID) -> None:
        """Soft delete de enfermedad."""
        await self.repo.eliminar(id, soft=True)
        await self.commit()