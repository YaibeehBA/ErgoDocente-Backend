"""
Logica de negocio para ArchivoMedia + integracion Cloudinary.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.archivos_media_repository import ArchivoMediaRepository
from app.core.exceptions import RecursoNoEncontradoError
from app.services.base import BaseService
from app.models.archivos_media import ArchivoMedia


class ArchivoMediaService(BaseService):
    """Service para gestion de archivos media con Cloudinary."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.archivos_media import ArchivoMedia
        self.repo = ArchivoMediaRepository(db, ArchivoMedia)

    async def subir(self, archivo_bytes: bytes, nombre: str, tipo_recurso: str, carpeta: str = "ergodocente") -> ArchivoMedia:
        """
        Subir archivo a Cloudinary y registrar en BD.
        Retorna el registro creado.
        """
        MAPA_CLOUDINARY = {
        "image": "image",
        "video": "video",
        "raw": "raw",
        "audio": "video",  # Cloudinary maneja audio como video
        }

       # Mapear tipo_recurso de Cloudinary a valores del enum en BD
        MAPA_TIPO_RECURSO = {
            "image": "imagen",
            "video": "video",
            "raw": "documento",
            "audio": "audio",
        }
        
        try:
            import cloudinary.uploader  # type: ignore
            resultado = cloudinary.uploader.upload(
                archivo_bytes,
                folder=carpeta,
                resource_type=MAPA_CLOUDINARY.get(tipo_recurso, "raw"),
                public_id=nombre,
            )
        except Exception as e:
            self.logger.error("cloudinary_upload_error", error=str(e))
            raise
        
        

        datos = {
            "public_id_cloudinary": resultado.get("public_id"),
            "url_publica": resultado.get("url"),
            "url_segura": resultado.get("secure_url"),
            "tipo_recurso": MAPA_TIPO_RECURSO.get(tipo_recurso, "imagen"),  
            "formato": resultado.get("format"),
            "tamano_bytes": resultado.get("bytes"),
            "ancho_px": resultado.get("width"),
            "alto_px": resultado.get("height"),
            "duracion_segundos": resultado.get("duration"),
            "carpeta_cloudinary": carpeta,
        }
        archivo = await self.repo.crear(datos)
        await self.commit()
        self.logger.info("archivo_subido", public_id=datos["public_id_cloudinary"])
        return archivo

    async def eliminar(self, id: UUID) -> None:
        """Eliminar archivo de Cloudinary y de la BD."""
        archivo = await self.repo.obtener_o_error(id)
        try:
            import cloudinary.uploader  # type: ignore
            cloudinary.uploader.destroy(archivo.public_id_cloudinary)
        except Exception as e:
            self.logger.error("cloudinary_delete_error", error=str(e))
        await self.repo.eliminar(id, soft=False)
        await self.commit()

    async def obtener_por_id(self, id: UUID):
        """Obtener archivo por ID."""
        return await self.repo.obtener_o_error(id)

    async def listar(self, page: int = 1, page_size: int = 20):
        """Listar archivos paginados."""
        return await self.repo.listar_paginado(page=page, page_size=page_size)