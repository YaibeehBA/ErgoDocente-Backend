"""
Repository para Traduccion (sistema polimorfico).
"""
from uuid import UUID
from sqlalchemy import select
from app.models.traducciones import Traduccion
from app.repositories.base import BaseRepository


class TraduccionRepository(BaseRepository[Traduccion]):
    """Repository especializado para Traduccion."""

    async def obtener_traducciones(
        self,
        tabla: str,
        registro_id: UUID,
        idioma_id: UUID | None = None,
    ) -> dict[str, str]:
        """
        Obtener todas las traducciones de un registro.
        Retorna dict: {campo: valor}.
        Si idioma_id es None, retorna en espanol.
        """
        query = select(Traduccion).where(
            Traduccion.tabla == tabla,
            Traduccion.registro_id == registro_id,
        )
        if idioma_id:
            query = query.where(Traduccion.idioma_id == idioma_id)
        result = await self.db.execute(query)
        traducciones = result.scalars().all()
        return {t.campo: t.valor for t in traducciones}

    async def obtener_traduccion_campo(
        self,
        tabla: str,
        registro_id: UUID,
        campo: str,
        idioma_id: UUID | None = None,
    ) -> str | None:
        """Obtener traduccion especifica de un campo."""
        stmt = select(Traduccion).where(
            Traduccion.tabla == tabla,
            Traduccion.registro_id == registro_id,
            Traduccion.campo == campo,
        )
        if idioma_id:
            stmt = stmt.where(Traduccion.idioma_id == idioma_id)
        result = await self.db.execute(stmt)
        traduccion = result.scalar_one_or_none()
        return traduccion.valor if traduccion else None