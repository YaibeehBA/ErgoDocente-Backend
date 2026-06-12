"""
Endpoints para preferencias por dispositivo.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import PreferenciasUsuarioResponse, PreferenciasUsuarioUpdateSchema
from app.services.preferencias_usuario_service import PreferenciasUsuarioService
from app.services.dispositivos_service import DispositivoService
from app.dependencies import get_db, get_device_id
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/preferencias", tags=["preferencias"])


@router.get("/mi-dispositivo", response_model=PreferenciasUsuarioResponse)
async def obtener_mis_preferencias(
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    service = PreferenciasUsuarioService(db)
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        return await service.obtener_por_dispositivo(dispositivo.id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/mi-dispositivo", response_model=PreferenciasUsuarioResponse)
async def actualizar_mis_preferencias(
    datos: PreferenciasUsuarioUpdateSchema,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    service = PreferenciasUsuarioService(db)
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        return await service.actualizar(dispositivo.id, datos.dict(exclude_unset=True))
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)