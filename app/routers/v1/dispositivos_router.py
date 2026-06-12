"""
Endpoints para registro y gestion de dispositivos.
Manejo de X-Device-ID header (V1 sin JWT).
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import DispositivoRegisterSchema, DispositivoResponse, DispositivosListResponse
from app.services.dispositivos_service import DispositivoService
from app.dependencies import get_db, get_device_id
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/dispositivos", tags=["dispositivos"])


@router.post("/registrar", response_model=DispositivoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_dispositivo(
    datos: DispositivoRegisterSchema,
    db: AsyncSession = Depends(get_db),
):
    service = DispositivoService(db)
    try:
        dispositivo = await service.registrar(datos.dict())
        return dispositivo
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/mi-dispositivo", response_model=DispositivoResponse)
async def obtener_mi_dispositivo(
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    service = DispositivoService(db)
    try:
        dispositivo = await service.obtener_por_device_id(device_id)
        return dispositivo
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dispositivo con device_id '{device_id}' no encontrado")


@router.get("/{id}", response_model=DispositivoResponse)
async def obtener_dispositivo(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = DispositivoService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("", response_model=DispositivosListResponse)
async def listar_dispositivos(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = DispositivoService(db)
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