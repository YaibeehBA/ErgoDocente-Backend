"""
Endpoints para subida y gestion de archivos multimedia.
Requiere Cloudinary configurado en .env
"""
import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ArchivoMediaResponse, ArchivosMediaListResponse
from app.services.archivos_media_service import ArchivoMediaService
from app.dependencies import get_db, get_device_id
from app.utils.file_validators import leer_y_validar_archivo, obtener_tipo_recurso_desde_mime
from app.core.exceptions import RecursoNoEncontradoError, CloudinaryError

router = APIRouter(prefix="/archivos-media", tags=["archivos-media"])


@router.post(
    "/subir",
    response_model=ArchivoMediaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Subir archivo multimedia a Cloudinary",
)
async def subir_archivo(
    archivo: UploadFile = File(..., description="Archivo a subir (imagen, video o audio/PDF)"),
    tipo_recurso: str = Form("image", description="Tipo: image, video, raw, audio"),
    carpeta: str = Form("ergodocente", description="Carpeta destino en Cloudinary"),
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Subir archivo a Cloudinary y registrar en base de datos.
    - **image**: JPEG, PNG, WEBP, GIF (max 5 MB)
    - **video**: MP4, MOV, AVI, WEBM (max 100 MB)
    - **raw**: PDF, MP3, WAV, OGG (max 10 MB)
    """
    # Leer y validar archivo
    try:
        contenido = await leer_y_validar_archivo(archivo, tipo_recurso)
    except HTTPException:
        raise

    # Generar nombre unico
    nombre_publico = f"{carpeta}/{uuid.uuid4().hex}"

    # Subir a Cloudinary y registrar en BD
    service = ArchivoMediaService(db)
    try:
        registro = await service.subir(
            archivo_bytes=contenido,
            nombre=nombre_publico,
            tipo_recurso=tipo_recurso,
            carpeta=carpeta,
        )
        return registro
    except CloudinaryError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el archivo: {str(e)}",
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar archivo de Cloudinary y BD",
)
async def eliminar_archivo(
    id: UUID,
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar archivo de Cloudinary y de la base de datos."""
    service = ArchivoMediaService(db)
    try:
        await service.eliminar(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except CloudinaryError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )


@router.get(
    "/{id}",
    response_model=ArchivoMediaResponse,
    summary="Obtener metadatos de un archivo",
)
async def obtener_archivo(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Obtener metadatos de un archivo por su ID."""
    service = ArchivoMediaService(db)
    try:
        return await service.obtener_por_id(id)
    except RecursoNoEncontradoError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    "",
    response_model=ArchivosMediaListResponse,
    summary="Listar archivos multimedia paginados",
)
async def listar_archivos(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """Listar todos los archivos multimedia registrados (admin)."""
    service = ArchivoMediaService(db)
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