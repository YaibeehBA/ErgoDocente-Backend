"""
Repository para ArchivoMedia (Cloudinary).
"""
from sqlalchemy import select
from app.models.archivos_media import ArchivoMedia
from app.repositories.base import BaseRepository


class ArchivoMediaRepository(BaseRepository[ArchivoMedia]):
    """Repository especializado para ArchivoMedia."""

    async def obtener_por_public_id(self, public_id: str) -> ArchivoMedia | None:
        """Obtener archivo por public_id_cloudinary (unique)."""
        stmt = select(ArchivoMedia).where(
            ArchivoMedia.public_id_cloudinary == public_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()