"""
Clase base para todos los seeders.
Provee metodos comunes: insertar, verificar existencia, logging.
"""
import asyncio
import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

logger = structlog.get_logger()


class BaseSeeder:
    """Seeder base con utilidades comunes."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.logger = logger.bind(seeder=self.__class__.__name__)
        self.insertados = 0
        self.omitidos = 0

    async def existe(self, modelo, **filtros) -> bool:
        """Verificar si ya existe un registro con los filtros dados."""
        query = select(modelo)
        for campo, valor in filtros.items():
            query = query.where(getattr(modelo, campo) == valor)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def obtener(self, modelo, **filtros):
        """Obtener registro por filtros."""
        query = select(modelo)
        for campo, valor in filtros.items():
            query = query.where(getattr(modelo, campo) == valor)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def insertar(self, modelo, datos: dict):
        """Insertar registro si no existe (idempotente)."""
        obj = modelo(**datos)
        self.db.add(obj)
        await self.db.flush()
        self.insertados += 1
        return obj

    async def seed(self) -> None:
        """Ejecutar seeder. Implementar en subclases."""
        raise NotImplementedError

    def log_resumen(self) -> None:
        """Imprimir resumen al finalizar."""
        self.logger.info(
            "seeder_completado",
            insertados=self.insertados,
            omitidos=self.omitidos,
        )