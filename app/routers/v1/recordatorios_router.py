"""
Endpoints para gestion de recordatorios por dispositivo.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import RecordatorioCreateSchema, RecordatorioUpdateSchema, RecordatorioResponse, RecordatoriosListResponse
from app.services.recordatorios_service import RecordatorioService
from app.services.dispositivos_service import DispositivoService
from app.dependencies import get_db, get_device_id
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/recordatorios", tags=["recordatorios"])


@router.post("", response_model=RecordatorioResponse, status_code=status.HTTP_201_CREATED)
async def crear_recordatorio(
    datos: RecordatorioCreateSchema,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        service = RecordatorioService(db)
        return await service.crear(dispositivo.id, datos.dict())
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("", response_model=RecordatoriosListResponse)
async def listar_mis_recordatorios(
    page: int = 1,
    page_size: int = 20,
    activos_solo: bool = False,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        service = RecordatorioService(db)
        
        if activos_solo:
            items = await service.listar_activos(dispositivo.id)
            total = len(items)
        else:
            items, total = await service.listar_por_dispositivo(dispositivo.id, page, page_size)
        
        pages = (total + page_size - 1) // page_size
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
            "has_next": page < pages,
        }
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/{id}", response_model=RecordatorioResponse)
async def actualizar_recordatorio(
    id: UUID,
    datos: RecordatorioUpdateSchema,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    service = RecordatorioService(db)
    try:
        return await service.actualizar(id, datos.dict(exclude_unset=True))
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/{id}/toggle", response_model=RecordatorioResponse)
async def toggle_recordatorio(
    id: UUID,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    service = RecordatorioService(db)
    try:
        return await service.toggle_activo(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_recordatorio(
    id: UUID,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    service = RecordatorioService(db)
    try:
        await service.eliminar(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)