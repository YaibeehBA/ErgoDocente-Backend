"""
Endpoints para rutinas de pausas activas.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import RutinaPausaActivaResponse, RutinasListResponse
from app.services.rutinas_pausas_activas_service import RutinaPausaActivaService
from app.dependencies import get_db
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/rutinas", tags=["rutinas"])


@router.get("", response_model=RutinasListResponse)
async def listar_rutinas(
    page: int = 1,
    page_size: int = 20,
    destacadas: bool = False,
    recomendadas: bool = False,
    db: AsyncSession = Depends(get_db),
):
    service = RutinaPausaActivaService(db)
    
    if destacadas:
        items, total = await service.listar_destacadas(page, page_size)
    elif recomendadas:
        items, total = await service.listar_recomendadas(page, page_size)
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


@router.get("/{id}", response_model=RutinaPausaActivaResponse)
async def obtener_rutina(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = RutinaPausaActivaService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)