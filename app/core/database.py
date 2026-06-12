from collections.abc import AsyncGenerator

import structlog
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

logger = structlog.get_logger(__name__)


# ── Motor Async ────────────────────────────────────────────────────────────────
engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,              # Verificar conexión antes de usarla
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    # Opciones específicas de asyncpg
    connect_args={
        "statement_cache_size": 0,   # Evitar problemas con pgbouncer en producción
        "prepared_statement_cache_size": 0,
    },
)

# ── Fábrica de Sesiones ────────────────────────────────────────────────────────
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,   # Evitar lazy-loading después de commit
    autocommit=False,
    autoflush=False,
)


# ── Funciones de ciclo de vida ─────────────────────────────────────────────────

async def init_db() -> None:
    """
    Inicializar la base de datos.
    En producción las migraciones se ejecutan con Alembic.
    Esto solo es para verificar conectividad.
    """
    async with engine.begin() as conn:
        logger.info("Conexión a PostgreSQL exitosa", database=settings.POSTGRES_DB)


async def close_db() -> None:
    """Cerrar el pool de conexiones al apagar la aplicación."""
    await engine.dispose()
    logger.info("Pool de conexiones PostgreSQL cerrado")


# ── Context Manager para conexión directa ─────────────────────────────────────

async def get_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Proporciona una conexión directa (para operaciones de bajo nivel)."""
    async with engine.begin() as conn:
        yield conn


# ── Dependency (se usa en app/dependencies/database.py) ───────────────────────

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency de FastAPI para inyectar sesión de base de datos.

    Uso:
        @router.get("/items")
        async def listar(db: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()