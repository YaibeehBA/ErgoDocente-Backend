"""
BaseRepository generico con CRUD y paginacion.
Todos los repositories heredan de aqui.
"""
from typing import Generic, TypeVar, Any, Protocol, runtime_checkable
from uuid import UUID
from sqlalchemy import select, func, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.exceptions import RecursoNoEncontradoError

T = TypeVar("T", bound=DeclarativeBase)

@runtime_checkable
class ConSoftDelete(Protocol):
    """Modelos que tienen soft-delete (eliminado_en + metodo eliminar)."""
    eliminado_en: Any  # columna DateTime nullable

    def eliminar(self) -> None: ...


@runtime_checkable
class ConTimestamp(Protocol):
    """Modelos que tienen columna creado_en."""
    creado_en: Any

class BaseRepository(Generic[T]):
    """Repository generico con operaciones CRUD."""

    def __init__(self, db: AsyncSession, model: type[T]):
        self.db = db
        self.model = model

    def _tiene_soft_delete(self) -> bool:
        return hasattr(self.model, "eliminado_en")

    def _columna_eliminado_en(self) -> Any:
        """Retorna la columna eliminado_en del modelo (solo si existe)."""
        return getattr(self.model, "eliminado_en")

    def _columna(self, nombre: str) -> Any:
        """Retorna una columna del modelo por nombre."""
        return getattr(self.model, nombre)

    async def crear(self, obj_in: dict) -> T:
        """Crear nuevo registro."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def obtener_por_id(self, id: UUID) -> T | None:
        """Obtener por ID primario."""
        return await self.db.get(self.model, id)

    async def obtener_o_error(self, id: UUID) -> T:
        """Obtener por ID o lanzar excepcion."""
        obj = await self.obtener_por_id(id)
        if obj is None:
            raise RecursoNoEncontradoError(self.model.__name__, id)
        return obj

    async def actualizar(self, id: UUID, obj_in: dict) -> T:
        """Actualizar registro."""
        db_obj = await self.obtener_o_error(id)
        for key, value in obj_in.items():
            if value is not None:
                setattr(db_obj, key, value)
        await self.db.flush()
        return db_obj

    async def eliminar(self, id: UUID, soft: bool = True) -> None:
        """Eliminar registro (soft delete por defecto)."""
        db_obj = await self.obtener_o_error(id)
        if soft and isinstance(db_obj, ConSoftDelete):
            db_obj.eliminar()          
        else:
            await self.db.delete(db_obj)

        await self.db.flush()

    async def listar_paginado(
        self,
        page: int = 1,
        page_size: int = 20,
        filtros: dict[str, Any] | None = None,
        order_by: str = "creado_en",
        order_direction: str = "desc",
        incluir_eliminados: bool = False,
    ) -> tuple[list[T], int]:
        """Listar con paginacion, filtros y ordenamiento."""
        query = select(self.model)

        # --- Soft delete filter ---
        if not incluir_eliminados and self._tiene_soft_delete():
            col_eliminado: ColumnElement[Any] = self._columna_eliminado_en()
            query = query.where(col_eliminado.is_(None))

        # --- Filtros dinamicos ---
        if filtros:
            for campo, valor in filtros.items():
                if hasattr(self.model, campo) and valor is not None:
                    query = query.where(self._columna(campo) == valor)

        # --- Contar total (antes de paginar) ---
        count_stmt = select(func.count()).select_from(self.model)
        if not incluir_eliminados and self._tiene_soft_delete():
            col_eliminado = self._columna_eliminado_en()
            count_stmt = count_stmt.where(col_eliminado.is_(None))
        if filtros:
            for campo, valor in filtros.items():
                if hasattr(self.model, campo) and valor is not None:
                    count_stmt = count_stmt.where(self._columna(campo) == valor)

        result_count = await self.db.execute(count_stmt)
        total: int = result_count.scalar() or 0

        # --- Ordenamiento ---
        if hasattr(self.model, order_by):
            order_col = self._columna(order_by)
            if order_direction.lower() == "asc":
                query = query.order_by(order_col.asc())
            else:
                query = query.order_by(order_col.desc())

        # --- Paginacion ---
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self.db.execute(query)
        items: list[T] = list(result.scalars().all())

        return items, total

  
    async def contar(self, filtros: dict[str, Any] | None = None) -> int:
        """Contar registros con filtros opcionales."""
        query = select(func.count()).select_from(self.model)
        if filtros:
            for campo, valor in filtros.items():
                if hasattr(self.model, campo) and valor is not None:
                    query = query.where(self._columna(campo) == valor)
        result = await self.db.execute(query)
        return result.scalar() or 0