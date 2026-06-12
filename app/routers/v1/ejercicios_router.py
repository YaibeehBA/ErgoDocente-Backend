"""
Endpoints para catalogo de ejercicios.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import EjercicioResponse, EjerciciosListResponse
from app.services.ejercicios_service import EjercicioService
from app.dependencies import get_db
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/ejercicios", tags=["ejercicios"])


@router.get("", response_model=EjerciciosListResponse)
async def listar_ejercicios(
    page: int = 1,
    page_size: int = 20,
    categoria_id: UUID | None = None,
    parte_cuerpo: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = EjercicioService(db)
    
    if categoria_id:
        items, total = await service.listar_por_categoria(categoria_id, page, page_size)
    elif parte_cuerpo:
        items, total = await service.listar_por_parte_cuerpo(parte_cuerpo, page, page_size)
    else:
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


@router.get("/{id}", response_model=EjercicioResponse)
async def obtener_ejercicio(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = EjercicioService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)