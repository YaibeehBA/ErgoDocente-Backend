"""
Datos iniciales: rutinas de pausas activas con traducciones.
"""
import uuid
from app.models.rutinas_pausas_activas import RutinaPausaActiva
from app.models.traducciones import Traduccion
from seeders.base_seeder import BaseSeeder

ID_IDIOMA_ES = uuid.UUID("00000000-0000-0000-0000-000000000001")
ID_IDIOMA_KW = uuid.UUID("00000000-0000-0000-0000-000000000002")

RUTINAS = [
    {
        "id": uuid.UUID("40000000-0000-0000-0000-000000000001"),
        "slug": "pausa-activa-5-minutos",
        "duracion_total_minutos": 5,
        "nivel_dificultad": "principiante",
        "esta_publicado": True,
        "es_predeterminado": True,
        "esta_destacado": True,
        "veces_completada": 0,
        "traducciones": {
            "titulo": {"es": "Pausa Activa de 5 Minutos", "kw": "5 minutopi samarichina"},
            "descripcion": {"es": "Rutina rapida para liberar tension y reactivar el cuerpo durante la jornada laboral", "kw": "Alli samarichina ruray"},
        },
    },
    {
        "id": uuid.UUID("40000000-0000-0000-0000-000000000002"),
        "slug": "pausa-visual-completa",
        "duracion_total_minutos": 3,
        "nivel_dificultad": "principiante",
        "esta_publicado": True,
        "es_predeterminado": False,
        "esta_destacado": True,
        "veces_completada": 0,
        "traducciones": {
            "titulo": {"es": "Pausa Visual Completa", "kw": "Ã‘awi samarichina"},
            "descripcion": {"es": "Rutina para descansar los ojos despues de largo tiempo frente a pantallas", "kw": "Ã‘awita samarichina"},
        },
    },
    {
        "id": uuid.UUID("40000000-0000-0000-0000-000000000003"),
        "slug": "rutina-antistres",
        "duracion_total_minutos": 10,
        "nivel_dificultad": "principiante",
        "esta_publicado": True,
        "es_predeterminado": False,
        "esta_destacado": True,
        "veces_completada": 0,
        "traducciones": {
            "titulo": {"es": "Rutina Anti-EstrÃ©s", "kw": "Llaki anchuchina"},
            "descripcion": {"es": "Combinacion de respiracion y estiramientos para reducir el estres laboral", "kw": "Samay shinari llakita anchuchina"},
        },
    },
]


class RutinasPausasActivasSeeder(BaseSeeder):
    """Seeder para rutinas de pausas activas con traducciones."""

    async def seed(self) -> None:
        for datos in RUTINAS:
            traducciones = datos.pop("traducciones")

            if await self.existe(RutinaPausaActiva, slug=datos["slug"]):
                self.logger.info("rutina_omitida", slug=datos["slug"])
                self.omitidos += 1
                datos["traducciones"] = traducciones
                continue

            rutina = await self.insertar(RutinaPausaActiva, datos)

            for campo, valores in traducciones.items():
                for codigo_idioma, valor in valores.items():
                    idioma_id = ID_IDIOMA_ES if codigo_idioma == "es" else ID_IDIOMA_KW
                    await self.insertar(Traduccion, {
                        "tabla": "rutinas_pausas_activas",
                        "registro_id": rutina.id,
                        "campo": campo,
                        "idioma_id": idioma_id,
                        "valor": valor,
                    })

            datos["traducciones"] = traducciones
            self.logger.info("rutina_insertada", slug=datos["slug"])

        self.log_resumen()