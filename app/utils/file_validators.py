"""
Validadores de tipo y tamano para archivos subidos por el usuario.
"""
from fastapi import UploadFile, HTTPException, status

# Tamanos maximos por tipo (en bytes)
TAMANO_MAX_IMAGEN = 5 * 1024 * 1024       # 5 MB
TAMANO_MAX_VIDEO = 100 * 1024 * 1024      # 100 MB
TAMANO_MAX_DOCUMENTO = 10 * 1024 * 1024   # 10 MB

# Tipos MIME permitidos por categoria
MIME_IMAGENES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}

MIME_VIDEOS = {
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo",
    "video/webm",
}

MIME_AUDIOS = {
    "audio/mpeg",   
    "audio/wav",
    "audio/ogg",
}

MIME_DOCUMENTOS = {
    "application/pdf",
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
}

# Mapa tipo_recurso â†’ (mimes permitidos, tamano maximo, label)
REGLAS_POR_TIPO: dict[str, tuple[set[str], int, str]] = {
    "image": (MIME_IMAGENES, TAMANO_MAX_IMAGEN, "imagen"),
    "video": (MIME_VIDEOS, TAMANO_MAX_VIDEO, "video"),
    "raw": (MIME_DOCUMENTOS, TAMANO_MAX_DOCUMENTO, "documento/audio"),
    "audio": (MIME_DOCUMENTOS, TAMANO_MAX_DOCUMENTO, "audio"),
}


def validar_archivo(archivo: UploadFile, tipo_recurso: str) -> None:
    """
    Validar tipo MIME y tamano de un archivo subido.

    Args:
        archivo: Archivo recibido en el endpoint (FastAPI UploadFile).
        tipo_recurso: 'image', 'video' o 'raw'.

    Raises:
        HTTPException 400: Si el tipo MIME no esta permitido.
        HTTPException 413: Si el archivo supera el tamano maximo.
        HTTPException 400: Si el tipo_recurso no es valido.
    """
    if tipo_recurso not in REGLAS_POR_TIPO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"tipo_recurso invalido: '{tipo_recurso}'. Valores permitidos: image, video, raw",
        )

    mimes_permitidos, tamano_max, label = REGLAS_POR_TIPO[tipo_recurso]

    # Validar tipo MIME
    content_type = archivo.content_type or ""
    if content_type not in mimes_permitidos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Tipo de archivo no permitido para {label}: '{content_type}'. "
                f"Permitidos: {sorted(mimes_permitidos)}"
            ),
        )

    # Validar tamano (si el archivo tiene size disponible)
    if hasattr(archivo, "size") and archivo.size is not None:
        if archivo.size > tamano_max:
            tamano_mb = tamano_max // (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"El archivo supera el tamano maximo permitido de {tamano_mb} MB para {label}",
            )


async def leer_y_validar_archivo(
    archivo: UploadFile,
    tipo_recurso: str,
) -> bytes:
    """
    Leer el contenido del archivo y validar tipo + tamano.
    Para tamanos no disponibles en UploadFile.size, valida despues de leer.

    Args:
        archivo: Archivo recibido en el endpoint.
        tipo_recurso: 'image', 'video' o 'raw'.

    Returns:
        Contenido binario del archivo.

    Raises:
        HTTPException: Si no pasa las validaciones.
    """
    # Validar tipo MIME primero (barato)
    validar_archivo(archivo, tipo_recurso)

    # Leer contenido
    contenido = await archivo.read()

    # Validar tamano real (por si UploadFile.size no estaba disponible)
    _, tamano_max, label = REGLAS_POR_TIPO[tipo_recurso]
    if len(contenido) > tamano_max:
        tamano_mb = tamano_max // (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"El archivo supera el tamano maximo permitido de {tamano_mb} MB para {label}",
        )

    return contenido


def obtener_tipo_recurso_desde_mime(content_type: str) -> str:
    """
    Inferir tipo_recurso de Cloudinary desde el MIME type.

    Args:
        content_type: MIME type del archivo (ej: 'image/jpeg').

    Returns:
        'image', 'video' o 'raw'.
    """
    if content_type in MIME_IMAGENES:
        return "image"
    if content_type in MIME_VIDEOS:
        return "video"
    return "raw"