"""
BaseService generico.
Todos los services heredan de aqui.
El commit se hace en el Service, no en el Repository.
"""
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger()


class BaseService:
    """Service base con sesion de base de datos y logging."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.logger = logger.bind(service=self.__class__.__name__)

    async def commit(self) -> None:
        """Confirmar transaccion."""
        await self.db.commit()

    async def rollback(self) -> None:
        """Revertir transaccion."""
        await self.db.rollback()