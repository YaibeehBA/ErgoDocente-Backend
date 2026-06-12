"""
Endpoints para catalogo de emociones.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import EmocionResponse, EmocionesListResponse
from app.services.emociones_service import EmocionService
from app.dependencies import get_db
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/emociones", tags=["emociones"])


@router.get("", response_model=EmocionesListResponse)
async def listar_emociones(
    page: int = 1,
    page_size: int = 20,
    positivas_solo: bool = False,
    db: AsyncSession = Depends(get_db),
):
    service = EmocionService(db)
    
    if positivas_solo:
        items, total = await service.listar_positivas(page, page_size)
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


@router.get("/{id}", response_model=EmocionResponse)
async def obtener_emocion(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = EmocionService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)