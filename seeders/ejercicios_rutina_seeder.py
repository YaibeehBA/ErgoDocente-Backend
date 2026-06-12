"""
Datos iniciales: asignacion de ejercicios a rutinas (tabla pivote).
"""
import uuid
from app.models.ejercicios_rutina import EjercicioRutina
from seeders.base_seeder import BaseSeeder

# IDs rutinas
RUTINA_5MIN     = uuid.UUID("40000000-0000-0000-0000-000000000001")
RUTINA_VISUAL   = uuid.UUID("40000000-0000-0000-0000-000000000002")
RUTINA_ANTISTRES = uuid.UUID("40000000-0000-0000-0000-000000000003")

# IDs ejercicios
EJ_CUELLO       = uuid.UUID("30000000-0000-0000-0000-000000000001")
EJ_HOMBROS      = uuid.UUID("30000000-0000-0000-0000-000000000002")
EJ_ESPALDA      = uuid.UUID("30000000-0000-0000-0000-000000000003")
EJ_MUNECAS      = uuid.UUID("30000000-0000-0000-0000-000000000004")
EJ_OJOS         = uuid.UUID("30000000-0000-0000-0000-000000000005")
EJ_RESP         = uuid.UUID("30000000-0000-0000-0000-000000000006")
EJ_PIERNAS      = uuid.UUID("30000000-0000-0000-0000-000000000007")

EJERCICIOS_RUTINA = [
    # Rutina 5 minutos
    {"rutina_id": RUTINA_5MIN, "ejercicio_id": EJ_CUELLO,   "orden": 1, "descanso_segundos": 10, "es_obligatorio": True},
    {"rutina_id": RUTINA_5MIN, "ejercicio_id": EJ_HOMBROS,  "orden": 2, "descanso_segundos": 10, "es_obligatorio": True},
    {"rutina_id": RUTINA_5MIN, "ejercicio_id": EJ_MUNECAS,  "orden": 3, "descanso_segundos": 10, "es_obligatorio": True},
    {"rutina_id": RUTINA_5MIN, "ejercicio_id": EJ_RESP,     "orden": 4, "descanso_segundos": 0,  "es_obligatorio": True},

    # Rutina visual
    {"rutina_id": RUTINA_VISUAL, "ejercicio_id": EJ_OJOS,   "orden": 1, "descanso_segundos": 15, "es_obligatorio": True},
    {"rutina_id": RUTINA_VISUAL, "ejercicio_id": EJ_RESP,   "orden": 2, "descanso_segundos": 0,  "es_obligatorio": False},

    # Rutina anti-estres
    {"rutina_id": RUTINA_ANTISTRES, "ejercicio_id": EJ_RESP,     "orden": 1, "descanso_segundos": 15, "es_obligatorio": True},
    {"rutina_id": RUTINA_ANTISTRES, "ejercicio_id": EJ_CUELLO,   "orden": 2, "descanso_segundos": 10, "es_obligatorio": True},
    {"rutina_id": RUTINA_ANTISTRES, "ejercicio_id": EJ_ESPALDA,  "orden": 3, "descanso_segundos": 10, "es_obligatorio": True},
    {"rutina_id": RUTINA_ANTISTRES, "ejercicio_id": EJ_HOMBROS,  "orden": 4, "descanso_segundos": 10, "es_obligatorio": True},
    {"rutina_id": RUTINA_ANTISTRES, "ejercicio_id": EJ_PIERNAS,  "orden": 5, "descanso_segundos": 0,  "es_obligatorio": False},
]


class EjerciciosRutinaSeeder(BaseSeeder):
    """Seeder para asignacion de ejercicios a rutinas."""

    async def seed(self) -> None:
        for datos in EJERCICIOS_RUTINA:
            if await self.existe(
                EjercicioRutina,
                rutina_id=datos["rutina_id"],
                ejercicio_id=datos["ejercicio_id"],
            ):
                self.omitidos += 1
                continue

            await self.insertar(EjercicioRutina, datos)
            self.logger.info(
                "ejercicio_rutina_insertado",
                rutina_id=str(datos["rutina_id"])[:8],
                orden=datos["orden"],
            )

        self.log_resumen()