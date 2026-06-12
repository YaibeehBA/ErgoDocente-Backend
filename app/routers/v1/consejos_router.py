"""
Endpoints para consejos de salud y bienestar.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ConsejoResponse, ConsejosListResponse
from app.services.consejos_service import ConsejoService
from app.dependencies import get_db
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/consejos", tags=["consejos"])


@router.get("", response_model=ConsejosListResponse)
async def listar_consejos(
    page: int = 1,
    page_size: int = 20,
    categoria: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = ConsejoService(db)
    
    if categoria:
        items, total = await service.listar_por_categoria(categoria, page, page_size)
    else:
        items, total = await service.listar_publicados(page, page_size)
    
    pages = (total + page_size - 1) // page_size
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
        "has_next": page < pages,
    }


@router.get("/{id}", response_model=ConsejoResponse)
async def obtener_consejo(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = ConsejoService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)