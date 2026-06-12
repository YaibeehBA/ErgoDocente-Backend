"""
Datos iniciales: recomendaciones automaticas por estado emocional.
Vincula emociones con ejercicios y rutinas recomendadas.
"""
import uuid
from app.models.recomendaciones_emocionales import RecomendacionEmocional
from seeders.base_seeder import BaseSeeder

# IDs emociones
EMOCION_ESTRES      = uuid.UUID("10000000-0000-0000-0000-000000000002")
EMOCION_CANSANCIO   = uuid.UUID("10000000-0000-0000-0000-000000000004")
EMOCION_ANSIEDAD    = uuid.UUID("10000000-0000-0000-0000-000000000006")
EMOCION_FRUSTRACION = uuid.UUID("10000000-0000-0000-0000-000000000008")
EMOCION_ALEGRIA     = uuid.UUID("10000000-0000-0000-0000-000000000001")
EMOCION_MOTIVACION  = uuid.UUID("10000000-0000-0000-0000-000000000005")

# IDs ejercicios
EJ_RESP     = uuid.UUID("30000000-0000-0000-0000-000000000006")
EJ_CUELLO   = uuid.UUID("30000000-0000-0000-0000-000000000001")
EJ_ESPALDA  = uuid.UUID("30000000-0000-0000-0000-000000000003")

# IDs rutinas
RUTINA_ANTISTRES = uuid.UUID("40000000-0000-0000-0000-000000000003")
RUTINA_5MIN      = uuid.UUID("40000000-0000-0000-0000-000000000001")
RUTINA_VISUAL    = uuid.UUID("40000000-0000-0000-0000-000000000002")

RECOMENDACIONES = [
    # Para estres: respiracion primero, luego rutina anti-estres
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000001"),
        "emocion_id": EMOCION_ESTRES,
        "tipo_recomendacion": "ejercicio",
        "referencia_id": EJ_RESP,
        "razon": "La respiracion diafragmatica reduce rapidamente los niveles de cortisol",
        "prioridad": 1,
    },
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000002"),
        "emocion_id": EMOCION_ESTRES,
        "tipo_recomendacion": "rutina",
        "referencia_id": RUTINA_ANTISTRES,
        "razon": "La rutina anti-estres combina respiracion y estiramiento para alivio completo",
        "prioridad": 2,
    },
    # Para cansancio: pausa de 5 minutos
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000003"),
        "emocion_id": EMOCION_CANSANCIO,
        "tipo_recomendacion": "rutina",
        "referencia_id": RUTINA_5MIN,
        "razon": "Una pausa activa de 5 minutos reactiva el cuerpo y reduce la fatiga",
        "prioridad": 1,
    },
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000004"),
        "emocion_id": EMOCION_CANSANCIO,
        "tipo_recomendacion": "ejercicio",
        "referencia_id": EJ_ESPALDA,
        "razon": "El estiramiento de espalda alivia la tension acumulada por largas horas sentado",
        "prioridad": 2,
    },
    # Para ansiedad: respiracion
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000005"),
        "emocion_id": EMOCION_ANSIEDAD,
        "tipo_recomendacion": "ejercicio",
        "referencia_id": EJ_RESP,
        "razon": "La respiracion profunda activa el sistema nervioso parasimpatico reduciendo la ansiedad",
        "prioridad": 1,
    },
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000006"),
        "emocion_id": EMOCION_ANSIEDAD,
        "tipo_recomendacion": "rutina",
        "referencia_id": RUTINA_ANTISTRES,
        "razon": "La combinacion de movimiento y respiracion es efectiva para la ansiedad moderada",
        "prioridad": 2,
    },
    # Para frustracion: movimiento fisico
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000007"),
        "emocion_id": EMOCION_FRUSTRACION,
        "tipo_recomendacion": "rutina",
        "referencia_id": RUTINA_5MIN,
        "razon": "El movimiento fisico libera endorfinas que contrarrestan la frustracion",
        "prioridad": 1,
    },
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000008"),
        "emocion_id": EMOCION_FRUSTRACION,
        "tipo_recomendacion": "ejercicio",
        "referencia_id": EJ_CUELLO,
        "razon": "La tension del cuello es comun en estados de frustracion",
        "prioridad": 2,
    },
    # Para alegria: mantener el estado con rutina visual
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000009"),
        "emocion_id": EMOCION_ALEGRIA,
        "tipo_recomendacion": "rutina",
        "referencia_id": RUTINA_VISUAL,
        "razon": "Mantener el bienestar con ejercicios de descanso visual preventivo",
        "prioridad": 1,
    },
    # Para motivacion: aprovechar con rutina completa
    {
        "id": uuid.UUID("90000000-0000-0000-0000-000000000010"),
        "emocion_id": EMOCION_MOTIVACION,
        "tipo_recomendacion": "rutina",
        "referencia_id": RUTINA_5MIN,
        "razon": "Aprovechar el estado motivado para completar la pausa activa completa",
        "prioridad": 1,
    },
]


class RecomendacionesEmocionalesSeeder(BaseSeeder):
    """Seeder para recomendaciones automaticas por estado emocional."""

    async def seed(self) -> None:
        for datos in RECOMENDACIONES:
            if await self.existe(RecomendacionEmocional, id=datos["id"]):
                self.logger.info("recomendacion_omitida", id=str(datos["id"])[:8])
                self.omitidos += 1
                continue

            await self.insertar(RecomendacionEmocional, datos)
            self.logger.info(
                "recomendacion_insertada",
                emocion_id=str(datos["emocion_id"])[:8],
                tipo=datos["tipo_recomendacion"],
                prioridad=datos["prioridad"],
            )

        self.log_resumen()