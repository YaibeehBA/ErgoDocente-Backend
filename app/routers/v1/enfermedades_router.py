"""
Endpoints para catalogo de enfermedades ocupacionales.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import EnfermedadOcupacionalResponse, EnfermedadesOcupacionalesListResponse
from app.services.enfermedades_ocupacionales_service import EnfermedadOcupacionalService
from app.dependencies import get_db
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/enfermedades", tags=["enfermedades"])


@router.get("", response_model=EnfermedadesOcupacionalesListResponse)
async def listar_enfermedades(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = EnfermedadOcupacionalService(db)
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


@router.get("/{id}", response_model=EnfermedadOcupacionalResponse)
async def obtener_enfermedad(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = EnfermedadOcupacionalService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)