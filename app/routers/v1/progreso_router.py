"""
Endpoints para tracking de progreso y gamificacion.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProgresoUsuarioCreateSchema, ProgresoUsuarioResponse, ProgresoUsuarioListResponse
from app.services.progreso_usuario_service import ProgresoUsuarioService
from app.services.dispositivos_service import DispositivoService
from app.dependencies import get_db, get_device_id
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/progreso", tags=["progreso"])


@router.post("", response_model=ProgresoUsuarioResponse, status_code=status.HTTP_201_CREATED)
async def registrar_actividad(
    datos: ProgresoUsuarioCreateSchema,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        service = ProgresoUsuarioService(db)
        return await service.registrar_actividad(
            dispositivo.id,
            datos.tipo_actividad,
            datos.referencia_id,
            datos.tipo_referencia,
            datos.duracion_real_segundos,
            datos.completado,
            datos.porcentaje_completado,
        )
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("", response_model=ProgresoUsuarioListResponse)
async def listar_mi_progreso(
    page: int = 1,
    page_size: int = 20,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        service = ProgresoUsuarioService(db)
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


@router.get("/puntos", response_model=dict)
async def obtener_mis_puntos(
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        service = ProgresoUsuarioService(db)
        return await service.obtener_nivel(dispositivo.id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)