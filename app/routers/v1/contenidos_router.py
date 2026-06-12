"""
Endpoints para contenidos ergonomicos educativos.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ContenidoErgonomicoResponse, ContenidosErgonomicosListResponse
from app.services.contenidos_ergonomicos_service import ContenidoErgonomicoService
from app.dependencies import get_db
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/contenidos", tags=["contenidos"])


@router.get("", response_model=ContenidosErgonomicosListResponse)
async def listar_contenidos(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = ContenidoErgonomicoService(db)
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


@router.get("/{id}", response_model=ContenidoErgonomicoResponse)
async def obtener_contenido(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = ContenidoErgonomicoService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)