"""
Wrapper para operaciones con Cloudinary.
Subir, eliminar y obtener metadatos de archivos multimedia.
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Any

from app.core.config import settings
from app.core.exceptions import CloudinaryError

# Configurar Cloudinary al importar el modulo
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)

CARPETA_BASE = settings.CLOUDINARY_FOLDER_BASE

# Tipos de recurso permitidos
TIPOS_RECURSO = ("image", "video", "raw")

# Carpetas por tipo de recurso
CARPETAS = {
    "image": f"{CARPETA_BASE}/imagenes",
    "video": f"{CARPETA_BASE}/videos",
    "raw": f"{CARPETA_BASE}/documentos",
}


def subir_archivo(
    archivo_bytes: bytes,
    nombre_publico: str,
    tipo_recurso: str = "image",
    carpeta: str | None = None,
    transformaciones: dict | None = None,
) -> dict[str, Any]:
    """
    Subir archivo a Cloudinary.

    Args:
        archivo_bytes: Contenido binario del archivo.
        nombre_publico: Identificador publico en Cloudinary (sin extension).
        tipo_recurso: 'image', 'video' o 'raw'.
        carpeta: Carpeta en Cloudinary. Si es None usa carpeta por defecto segun tipo.
        transformaciones: Transformaciones opcionales (solo para imagenes).

    Returns:
        dict con: public_id, secure_url, format, bytes, width, height, duration.

    Raises:
        CloudinaryError: Si falla la subida.
    """
    if tipo_recurso not in TIPOS_RECURSO:
        raise CloudinaryError(f"Tipo de recurso invalido: {tipo_recurso}. Permitidos: {TIPOS_RECURSO}")

    carpeta_destino = carpeta or CARPETAS.get(tipo_recurso, "ergodocente/otros")

    opciones: dict[str, Any] = {
        "folder": carpeta_destino,
        "public_id": nombre_publico,
        "resource_type": tipo_recurso,
        "overwrite": True,
        "use_filename": False,
    }

    if transformaciones and tipo_recurso == "image":
        opciones["transformation"] = transformaciones

    try:
        resultado = cloudinary.uploader.upload(archivo_bytes, **opciones)
    except Exception as e:
        raise CloudinaryError(f"No se pudo subir el archivo: {str(e)}")

    return {
        "public_id": resultado.get("public_id", ""),
        "secure_url": resultado.get("secure_url", ""),
        "formato": resultado.get("format", ""),
        "bytes": resultado.get("bytes", 0),
        "ancho": resultado.get("width"),
        "alto": resultado.get("height"),
        "duracion": resultado.get("duration"),
        "tipo_recurso": resultado.get("resource_type", tipo_recurso),
    }


def eliminar_archivo(public_id: str, tipo_recurso: str = "image") -> bool:
    """
    Eliminar archivo de Cloudinary por su public_id.

    Args:
        public_id: Identificador publico del archivo en Cloudinary.
        tipo_recurso: 'image', 'video' o 'raw'.

    Returns:
        True si fue eliminado, False si no existia.

    Raises:
        CloudinaryError: Si falla la eliminacion.
    """
    try:
        resultado = cloudinary.uploader.destroy(
            public_id,
            resource_type=tipo_recurso,
        )
        return resultado.get("result") == "ok"
    except Exception as e:
        raise CloudinaryError(f"No se pudo eliminar el archivo '{public_id}': {str(e)}")


def obtener_metadatos(public_id: str, tipo_recurso: str = "image") -> dict[str, Any]:
    """
    Obtener metadatos de un archivo en Cloudinary.

    Args:
        public_id: Identificador publico del archivo.
        tipo_recurso: 'image', 'video' o 'raw'.

    Returns:
        dict con metadatos del archivo.

    Raises:
        CloudinaryError: Si el archivo no existe o falla la consulta.
    """
    try:
        resultado = cloudinary.api.resource(public_id, resource_type=tipo_recurso)
        return {
            "public_id": resultado.get("public_id"),
            "secure_url": resultado.get("secure_url"),
            "formato": resultado.get("format"),
            "bytes": resultado.get("bytes"),
            "ancho": resultado.get("width"),
            "alto": resultado.get("height"),
            "duracion": resultado.get("duration"),
            "creado_en": resultado.get("created_at"),
        }
    except Exception as e:
        raise CloudinaryError(f"No se pudo obtener metadatos de '{public_id}': {str(e)}")


def generar_url_transformada(
    public_id: str,
    ancho: int | None = None,
    alto: int | None = None,
    calidad: int = 80,
    formato: str = "webp",
) -> str:
    """
    Generar URL con transformaciones para imagen.
    Util para thumbnails y versiones optimizadas.

    Args:
        public_id: Identificador publico de la imagen.
        ancho: Ancho en pixeles (opcional).
        alto: Alto en pixeles (opcional).
        calidad: Calidad de compresion 1-100 (defecto: 80).
        formato: Formato de salida (defecto: webp).

    Returns:
        URL transformada de Cloudinary.
    """
    transformacion: dict[str, Any] = {
        "quality": calidad,
        "fetch_format": formato,
    }
    if ancho:
        transformacion["width"] = ancho
    if alto:
        transformacion["height"] = alto
    if ancho or alto:
        transformacion["crop"] = "fill"

    return cloudinary.CloudinaryImage(public_id).build_url(**transformacion)