"""
Script principal para ejecutar todos los seeders en orden correcto.
Uso: python -m seeders.run_seeders
"""
import asyncio
import structlog

from app.core.database import AsyncSessionLocal
from app.core.logging_config import setup_logging

from seeders.idiomas_seeder import IdiomasSeeder
from seeders.emociones_seeder import EmocionesSeeder
from seeders.categorias_ejercicios_seeder import CategoriasEjerciciosSeeder
from seeders.ejercicios_seeder import EjerciciosSeeder
from seeders.rutinas_pausas_activas_seeder import RutinasPausasActivasSeeder
from seeders.ejercicios_rutina_seeder import EjerciciosRutinaSeeder
from seeders.contenidos_ergonomicos_seeder import ContenidosErgonomicosSeeder
from seeders.enfermedades_ocupacionales_seeder import EnfermedadesOcupacionalesSeeder
from seeders.consejos_seeder import ConsejosSeeder
from seeders.mensajes_motivacionales_seeder import MensajesMotivacionalesSeeder
from seeders.recomendaciones_emocionales_seeder import RecomendacionesEmocionalesSeeder

logger = structlog.get_logger()


async def ejecutar_seeders() -> None:
    """Ejecutar todos los seeders en el orden correcto."""
    setup_logging()

    logger.info("seeders_inicio", mensaje="Iniciando carga de datos iniciales...")

    async with AsyncSessionLocal() as db:
        # ORDEN CRITICO: respetar dependencias entre tablas
        seeders = [
            # 1. Idiomas (sin dependencias)
            IdiomasSeeder(db),
            # 2. Emociones (sin dependencias, pero sus traducciones dependen de idiomas)
            EmocionesSeeder(db),
            # 3. Categorias de ejercicios (sin dependencias)
            CategoriasEjerciciosSeeder(db),
            # 4. Ejercicios (depende de categorias)
            EjerciciosSeeder(db),
            # 5. Rutinas (sin dependencias directas)
            RutinasPausasActivasSeeder(db),
            # 6. Ejercicios en rutinas (depende de ejercicios + rutinas)
            EjerciciosRutinaSeeder(db),
            # 7. Contenidos ergonomicos (sin dependencias)
            ContenidosErgonomicosSeeder(db),
            # 8. Enfermedades ocupacionales (sin dependencias)
            EnfermedadesOcupacionalesSeeder(db),
            # 9. Consejos (sin dependencias)
            ConsejosSeeder(db),
            # 10. Mensajes motivacionales (sin dependencias)
            MensajesMotivacionalesSeeder(db),
            # 11. Recomendaciones emocionales (depende de emociones + ejercicios + rutinas)
            RecomendacionesEmocionalesSeeder(db),
        ]

        for seeder in seeders:
            nombre = seeder.__class__.__name__
            logger.info("seeder_ejecutando", seeder=nombre)
            try:
                await seeder.seed()
                await db.commit()
                logger.info("seeder_ok", seeder=nombre)
            except Exception as e:
                await db.rollback()
                logger.error("seeder_error", seeder=nombre, error=str(e))
                raise

    logger.info("seeders_completados", mensaje="Todos los seeders ejecutados exitosamente")


if __name__ == "__main__":
    asyncio.run(ejecutar_seeders())