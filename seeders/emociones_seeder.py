"""
Datos iniciales: catalogo de emociones base.
Incluye traducciones al Kichwa.
"""
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.emociones import Emocion
from app.models.traducciones import Traduccion
from seeders.base_seeder import BaseSeeder

ID_IDIOMA_ES = uuid.UUID("00000000-0000-0000-0000-000000000001")
ID_IDIOMA_KW = uuid.UUID("00000000-0000-0000-0000-000000000002")

EMOCIONES = [
    {
        "id": uuid.UUID("10000000-0000-0000-0000-000000000001"),
        "slug": "alegria",
        "emoji": "ðŸ˜Š",
        "color_hex": "#FFD700",
        "nivel_intensidad": 4,
        "es_positiva": True,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "AlegrÃ­a", "kw": "Kushiy"},
            "descripcion": {"es": "Sentimiento de placer y bienestar", "kw": "Sumak kawsay ruraymi"},
        },
    },
    {
        "id": uuid.UUID("10000000-0000-0000-0000-000000000002"),
        "slug": "estres",
        "emoji": "ðŸ˜°",
        "color_hex": "#FF6B6B",
        "nivel_intensidad": 4,
        "es_positiva": False,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "EstrÃ©s", "kw": "Llaki"},
            "descripcion": {"es": "Tension y presion mental", "kw": "Shunkup nanay"},
        },
    },
    {
        "id": uuid.UUID("10000000-0000-0000-0000-000000000003"),
        "slug": "calma",
        "emoji": "ðŸ˜Œ",
        "color_hex": "#98D8C8",
        "nivel_intensidad": 2,
        "es_positiva": True,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "Calma", "kw": "Sumak shunkuy"},
            "descripcion": {"es": "Estado de tranquilidad y paz interior", "kw": "Alli shunkuy"},
        },
    },
    {
        "id": uuid.UUID("10000000-0000-0000-0000-000000000004"),
        "slug": "cansancio",
        "emoji": "ðŸ˜´",
        "color_hex": "#B8B8B8",
        "nivel_intensidad": 3,
        "es_positiva": False,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "Cansancio", "kw": "Sayki"},
            "descripcion": {"es": "Fatiga fisica o mental acumulada", "kw": "Uknay"},
        },
    },
    {
        "id": uuid.UUID("10000000-0000-0000-0000-000000000005"),
        "slug": "motivacion",
        "emoji": "ðŸ’ª",
        "color_hex": "#4CAF50",
        "nivel_intensidad": 5,
        "es_positiva": True,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "MotivaciÃ³n", "kw": "Kallpay"},
            "descripcion": {"es": "Energia y deseo de alcanzar metas", "kw": "Alli yuyay"},
        },
    },
    {
        "id": uuid.UUID("10000000-0000-0000-0000-000000000006"),
        "slug": "ansiedad",
        "emoji": "ðŸ˜Ÿ",
        "color_hex": "#FF9800",
        "nivel_intensidad": 4,
        "es_positiva": False,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "Ansiedad", "kw": "Manchay"},
            "descripcion": {"es": "Inquietud y preocupacion excesiva", "kw": "Manchay yuyay"},
        },
    },
    {
        "id": uuid.UUID("10000000-0000-0000-0000-000000000007"),
        "slug": "satisfaccion",
        "emoji": "ðŸ˜„",
        "color_hex": "#8BC34A",
        "nivel_intensidad": 4,
        "es_positiva": True,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "SatisfacciÃ³n", "kw": "Kusikuy"},
            "descripcion": {"es": "Sensacion de logro y cumplimiento", "kw": "Alli ruray"},
        },
    },
    {
        "id": uuid.UUID("10000000-0000-0000-0000-000000000008"),
        "slug": "frustracion",
        "emoji": "ðŸ˜¤",
        "color_hex": "#F44336",
        "nivel_intensidad": 3,
        "es_positiva": False,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "FrustraciÃ³n", "kw": "PiÃ±ay"},
            "descripcion": {"es": "Sensacion de bloqueo ante obstaculos", "kw": "Mana ushaymi"},
        },
    },
]


class EmocionesSeeder(BaseSeeder):
    """Seeder para catalogo de emociones con traducciones."""

    async def seed(self) -> None:
        """Insertar emociones y sus traducciones."""
        for datos in EMOCIONES:
            traducciones = datos.pop("traducciones")

            if await self.existe(Emocion, slug=datos["slug"]):
                self.logger.info("emocion_omitida", slug=datos["slug"])
                self.omitidos += 1
                datos["traducciones"] = traducciones
                continue

            emocion = await self.insertar(Emocion, datos)

            # Insertar traducciones
            for campo, valores in traducciones.items():
                for codigo_idioma, valor in valores.items():
                    idioma_id = ID_IDIOMA_ES if codigo_idioma == "es" else ID_IDIOMA_KW
                    await self.insertar(Traduccion, {
                        "tabla": "emociones",
                        "registro_id": emocion.id,
                        "campo": campo,
                        "idioma_id": idioma_id,
                        "valor": valor,
                    })

            datos["traducciones"] = traducciones
            self.logger.info("emocion_insertada", slug=datos["slug"])

        self.log_resumen()