"""
Endpoints para idiomas disponibles (Espanol, Kichwa).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import IdiomaResponse, IdiomasListResponse
from app.services.idiomas_service import IdiomaService
from app.dependencies import get_db
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/idiomas", tags=["idiomas"])


@router.get("", response_model=IdiomasListResponse)
async def listar_idiomas(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = IdiomaService(db)
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


@router.get("/{codigo}", response_model=IdiomaResponse)
async def obtener_idioma(
    codigo: str,
    db: AsyncSession = Depends(get_db),
):
    service = IdiomaService(db)
    try:
        return await service.obtener_por_codigo(codigo)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/predeterminado", response_model=IdiomaResponse)
async def obtener_idioma_predeterminado(
    db: AsyncSession = Depends(get_db),
):
    service = IdiomaService(db)
    idioma = await service.obtener_predeterminado()
    if not idioma:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return idioma