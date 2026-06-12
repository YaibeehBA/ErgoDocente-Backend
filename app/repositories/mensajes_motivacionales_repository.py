"""
Repository para MensajeMotivacional.
"""
from sqlalchemy import select, func
from app.models.mensajes_motivacionales import MensajeMotivacional
from app.repositories.base import BaseRepository


class MensajeMotivacionalRepository(BaseRepository[MensajeMotivacional]):
    """Repository especializado para MensajeMotivacional."""

    async def listar_por_categoria(
        self,
        categoria: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """Listar mensajes por categoria publicados."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"categoria": categoria, "esta_publicado": True},
        )

    async def listar_publicados(self, page: int = 1, page_size: int = 20) -> tuple[list, int]:
        """Listar todos los mensajes publicados."""
        return await self.listar_paginado(
            page=page,
            page_size=page_size,
            filtros={"esta_publicado": True},
        )

    async def obtener_aleatorio(self) -> MensajeMotivacional | None:
        """Obtener un mensaje motivacional aleatorio publicado."""
        stmt = select(MensajeMotivacional).where(
            MensajeMotivacional.esta_publicado == True,
            MensajeMotivacional.eliminado_en.is_(None),
        ).order_by(func.random()).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()