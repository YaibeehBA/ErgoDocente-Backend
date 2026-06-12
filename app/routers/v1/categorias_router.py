"""
Endpoints para categorias de ejercicios.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import CategoriaEjercicioResponse, CategoriasEjerciciosListResponse
from app.services.categorias_ejercicios_service import CategoriaEjercicioService
from app.dependencies import get_db
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("", response_model=CategoriasEjerciciosListResponse)
async def listar_categorias(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = CategoriaEjercicioService(db)
    items, total = await service.listar(page, page_size)
    pages = (total + page_size - 1) // page_size
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
        "has_next": page < pages,
    }


@router.get("/{id}", response_model=CategoriaEjercicioResponse)
async def obtener_categoria(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = CategoriaEjercicioService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)