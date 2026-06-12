"""
Datos iniciales: categorias de ejercicios con traducciones.
"""
import uuid
from app.models.categorias_ejercicios import CategoriaEjercicio
from app.models.traducciones import Traduccion
from seeders.base_seeder import BaseSeeder

ID_IDIOMA_ES = uuid.UUID("00000000-0000-0000-0000-000000000001")
ID_IDIOMA_KW = uuid.UUID("00000000-0000-0000-0000-000000000002")

CATEGORIAS = [
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000001"),
        "slug": "cuello-y-hombros",
        "color_hex": "#2196F3",
        "orden": 1,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "Cuello y Hombros", "kw": "Kunka muyuchina"},
            "descripcion": {"es": "Ejercicios para aliviar tension en cuello y hombros", "kw": "Kunka shunkuy allichina"},
        },
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000002"),
        "slug": "espalda",
        "color_hex": "#4CAF50",
        "orden": 2,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "Espalda", "kw": "Wasa"},
            "descripcion": {"es": "Ejercicios para fortalecer y relajar la espalda", "kw": "Wasa kallpachina"},
        },
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000003"),
        "slug": "munecas-y-manos",
        "color_hex": "#FF9800",
        "orden": 3,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "MuÃ±ecas y Manos", "kw": "Maki"},
            "descripcion": {"es": "Ejercicios para prevenir lesiones en manos y munecas", "kw": "Maki wanuchina"},
        },
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000004"),
        "slug": "ojos-y-vision",
        "color_hex": "#9C27B0",
        "orden": 4,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "Ojos y VisiÃ³n", "kw": "Ã‘awi"},
            "descripcion": {"es": "Ejercicios para descansar y fortalecer la vista", "kw": "Ã‘awi samarichina"},
        },
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000005"),
        "slug": "respiracion",
        "color_hex": "#00BCD4",
        "orden": 5,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "RespiraciÃ³n", "kw": "Samay"},
            "descripcion": {"es": "Tecnicas de respiracion para reducir el estres", "kw": "Samay allichina"},
        },
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000006"),
        "slug": "piernas-y-pies",
        "color_hex": "#795548",
        "orden": 6,
        "esta_activo": True,
        "traducciones": {
            "nombre": {"es": "Piernas y Pies", "kw": "Chaki"},
            "descripcion": {"es": "Ejercicios para activar la circulacion en piernas", "kw": "Chaki kawsachina"},
        },
    },
]


class CategoriasEjerciciosSeeder(BaseSeeder):
    """Seeder para categorias de ejercicios con traducciones."""

    async def seed(self) -> None:
        for datos in CATEGORIAS:
            traducciones = datos.pop("traducciones")

            if await self.existe(CategoriaEjercicio, slug=datos["slug"]):
                self.logger.info("categoria_omitida", slug=datos["slug"])
                self.omitidos += 1
                datos["traducciones"] = traducciones
                continue

            categoria = await self.insertar(CategoriaEjercicio, datos)

            for campo, valores in traducciones.items():
                for codigo_idioma, valor in valores.items():
                    idioma_id = ID_IDIOMA_ES if codigo_idioma == "es" else ID_IDIOMA_KW
                    await self.insertar(Traduccion, {
                        "tabla": "categorias_ejercicios",
                        "registro_id": categoria.id,
                        "campo": campo,
                        "idioma_id": idioma_id,
                        "valor": valor,
                    })

            datos["traducciones"] = traducciones
            self.logger.info("categoria_insertada", slug=datos["slug"])

        self.log_resumen()