"""
Endpoints para mensajes motivacionales.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import MensajeMotivacionalResponse, MensajesMotivacionalesListResponse
from app.services.mensajes_motivacionales_service import MensajeMotivacionalService
from app.dependencies import get_db
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/mensajes-motivacionales", tags=["mensajes"])


@router.get("", response_model=MensajesMotivacionalesListResponse)
async def listar_mensajes(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = MensajeMotivacionalService(db)
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


@router.get("/aleatorio", response_model=MensajeMotivacionalResponse)
async def obtener_mensaje_aleatorio(
    db: AsyncSession = Depends(get_db),
):
    service = MensajeMotivacionalService(db)
    mensaje = await service.obtener_aleatorio()
    if not mensaje:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return mensaje


@router.get("/{id}", response_model=MensajeMotivacionalResponse)
async def obtener_mensaje(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = MensajeMotivacionalService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)