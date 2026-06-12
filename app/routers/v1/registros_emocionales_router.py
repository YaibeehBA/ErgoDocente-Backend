"""
Endpoints para tracking emocional y recomendaciones automaticas.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import RegistroEmocionalCreateSchema, RegistroEmocionalResponse, RegistrosEmocionalListResponse
from app.services.registros_emocionales_service import RegistroEmocionalService
from app.services.dispositivos_service import DispositivoService
from app.dependencies import get_db, get_device_id
from app.core.exceptions import RecursoNoEncontradoError

router = APIRouter(prefix="/registros-emocionales", tags=["registros-emocionales"])

@router.post("", response_model=RegistroEmocionalResponse, status_code=status.HTTP_201_CREATED)
async def registrar_emocion(
    datos: RegistroEmocionalCreateSchema,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        service = RegistroEmocionalService(db)
        campos_validos = {"emocion_id", "intensidad", "nota", "contexto"}
        datos_filtrados = {k: v for k, v in datos.dict().items() if k in campos_validos and v is not None}
        return await service.registrar(dispositivo.id, datos_filtrados)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.get("", response_model=RegistrosEmocionalListResponse)
async def listar_mis_registros_emocionales(
    page: int = 1,
    page_size: int = 20,
    ultimas_horas: int | None = None,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        service = RegistroEmocionalService(db)
        
        if ultimas_horas:
            items = await service.listar_ultimas_24h(dispositivo.id)
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


@router.get("/estadisticas", response_model=dict)
async def obtener_estadisticas_emocionales(
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        disp_service = DispositivoService(db)
        dispositivo = await disp_service.obtener_por_device_id(device_id)
        service = RegistroEmocionalService(db)
        return await service.obtener_estadisticas(dispositivo.id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)