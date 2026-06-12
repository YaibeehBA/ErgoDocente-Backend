"""
Datos iniciales: consejos de salud y bienestar con traducciones.
"""
import uuid
from app.models.consejos import Consejo
from app.models.traducciones import Traduccion
from seeders.base_seeder import BaseSeeder

ID_IDIOMA_ES = uuid.UUID("00000000-0000-0000-0000-000000000001")
ID_IDIOMA_KW = uuid.UUID("00000000-0000-0000-0000-000000000002")

CONSEJOS = [
    {
        "id": uuid.UUID("70000000-0000-0000-0000-000000000001"),
        "slug": "hidratacion-durante-trabajo",
        "categoria": "hidratacion",
        "esta_publicado": True,
        "orden": 1,
        "traducciones": {
            "titulo": {"es": "Mantente Hidratado en el Trabajo", "kw": "Yakuta upiy llankaypim"},
            "descripcion": {"es": "Bebe al menos 8 vasos de agua al dia para mantener tu concentracion y energia", "kw": "8 vaso yakuta upiy"},
            "contenido": {"es": "La deshidratacion reduce la concentracion hasta en un 20%. Ten siempre agua en tu escritorio.", "kw": "Yaku illakpika mana yuyayta ushanki"},
        },
    },
    {
        "id": uuid.UUID("70000000-0000-0000-0000-000000000002"),
        "slug": "posicion-monitor-ergonomica",
        "categoria": "ergonomia",
        "esta_publicado": True,
        "orden": 2,
        "traducciones": {
            "titulo": {"es": "PosiciÃ³n Correcta del Monitor", "kw": "Pantallata alli churana"},
            "descripcion": {"es": "Coloca el monitor a la altura de los ojos para evitar tension cervical", "kw": "Pantallata Ã±awi karu churay"},
            "contenido": {"es": "El borde superior del monitor debe estar a la altura de los ojos, a 50-70 cm de distancia.", "kw": "Pantalla hawapi Ã±awi chayana"},
        },
    },
    {
        "id": uuid.UUID("70000000-0000-0000-0000-000000000003"),
        "slug": "descansos-regulares",
        "categoria": "productividad",
        "esta_publicado": True,
        "orden": 3,
        "traducciones": {
            "titulo": {"es": "Toma Descansos Regulares", "kw": "Alli samarichina"},
            "descripcion": {"es": "Levantate cada 45-60 minutos para mejorar la circulacion y reducir la fatiga", "kw": "60 minutopi samarichina"},
            "contenido": {"es": "Cada hora de trabajo sentado aumenta el riesgo de problemas cardiovasculares. Usa la tecnica Pomodoro.", "kw": "Tiyarispa llankay llakita ruran"},
        },
    },
    {
        "id": uuid.UUID("70000000-0000-0000-0000-000000000004"),
        "slug": "iluminacion-adecuada",
        "categoria": "ergonomia",
        "esta_publicado": True,
        "orden": 4,
        "traducciones": {
            "titulo": {"es": "IluminaciÃ³n Adecuada en tu Espacio", "kw": "Alli llankana kaway"},
            "descripcion": {"es": "Una buena iluminacion reduce la fatiga visual y mejora la productividad", "kw": "Alli kanchay Ã±awita wanuchina"},
            "contenido": {"es": "Evita reflejos en la pantalla. La luz natural es ideal, complementada con luz artificial indirecta.", "kw": "Alli kanchaypi llankay"},
        },
    },
    {
        "id": uuid.UUID("70000000-0000-0000-0000-000000000005"),
        "slug": "manejo-estres-tecnicas",
        "categoria": "bienestar",
        "esta_publicado": True,
        "orden": 5,
        "traducciones": {
            "titulo": {"es": "TÃ©cnicas para Manejar el EstrÃ©s", "kw": "Llakita anchuchina"},
            "descripcion": {"es": "Aprende tecnicas sencillas para reducir el estres laboral cotidiano", "kw": "Llakita anchuchina yachana"},
            "contenido": {"es": "La respiracion profunda, la meditacion y el ejercicio fisico son las tres tecnicas mas efectivas.", "kw": "Samay, yuyay, kallpachina"},
        },
    },
]


class ConsejosSeeder(BaseSeeder):
    """Seeder para consejos de salud y bienestar."""

    async def seed(self) -> None:
        for datos in CONSEJOS:
            traducciones = datos.pop("traducciones")

            if await self.existe(Consejo, slug=datos["slug"]):
                self.logger.info("consejo_omitido", slug=datos["slug"])
                self.omitidos += 1
                datos["traducciones"] = traducciones
                continue

            consejo = await self.insertar(Consejo, datos)

            for campo, valores in traducciones.items():
                for codigo_idioma, valor in valores.items():
                    idioma_id = ID_IDIOMA_ES if codigo_idioma == "es" else ID_IDIOMA_KW
                    await self.insertar(Traduccion, {
                        "tabla": "consejos",
                        "registro_id": consejo.id,
                        "campo": campo,
                        "idioma_id": idioma_id,
                        "valor": valor,
                    })

            datos["traducciones"] = traducciones
            self.logger.info("consejo_insertado", slug=datos["slug"])

        self.log_resumen()