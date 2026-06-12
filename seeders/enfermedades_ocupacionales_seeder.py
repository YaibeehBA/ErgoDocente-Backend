"""
Datos iniciales: catalogo de enfermedades ocupacionales con traducciones.
"""
import uuid
from app.models.enfermedades_ocupacionales import EnfermedadOcupacional
from app.models.traducciones import Traduccion
from seeders.base_seeder import BaseSeeder

ID_IDIOMA_ES = uuid.UUID("00000000-0000-0000-0000-000000000001")
ID_IDIOMA_KW = uuid.UUID("00000000-0000-0000-0000-000000000002")

ENFERMEDADES = [
    {
        "id": uuid.UUID("60000000-0000-0000-0000-000000000001"),
        "slug": "sindrome-tunel-carpiano",
        "categoria": "musculoesqueletica",
        "codigo_cie10": "G56.0",
        "esta_publicado": True,
        "traducciones": {
            "nombre": {"es": "SÃ­ndrome del TÃºnel Carpiano", "kw": "Maki unchiy"},
            "descripcion": {"es": "Compresion del nervio mediano en la muneca causada por movimientos repetitivos", "kw": "Maki llakiy"},
            "sintomas": {"es": "Dolor, hormigueo y entumecimiento en la mano y dedos", "kw": "Maki nanay, charishka"},
            "prevencion": {"es": "Pausas activas, ejercicios de muneca, posicion ergonomica del teclado", "kw": "Maki samarichina"},
        },
    },
    {
        "id": uuid.UUID("60000000-0000-0000-0000-000000000002"),
        "slug": "lumbalgia-cronica",
        "categoria": "musculoesqueletica",
        "codigo_cie10": "M54.5",
        "esta_publicado": True,
        "traducciones": {
            "nombre": {"es": "Lumbalgia CrÃ³nica", "kw": "Wasa nanay"},
            "descripcion": {"es": "Dolor cronico en la zona lumbar por sedentarismo prolongado", "kw": "Wasa llakiy"},
            "sintomas": {"es": "Dolor persistente en la parte baja de la espalda, rigidez matutina", "kw": "Ura wasa nanay"},
            "prevencion": {"es": "Postura correcta, pausas activas, silla ergonomica, ejercicio regular", "kw": "Alli tiyarina, samarichina"},
        },
    },
    {
        "id": uuid.UUID("60000000-0000-0000-0000-000000000003"),
        "slug": "fatiga-visual-digital",
        "categoria": "visual",
        "codigo_cie10": "H53.1",
        "esta_publicado": True,
        "traducciones": {
            "nombre": {"es": "Fatiga Visual Digital", "kw": "Ã‘awi sayki"},
            "descripcion": {"es": "Cansancio ocular por exposicion prolongada a pantallas digitales", "kw": "Ã‘awi llakiy pantallapi"},
            "sintomas": {"es": "Vista borrosa, ojos secos, dolor de cabeza, sensibilidad a la luz", "kw": "Ã‘awi nanay, uma nanay"},
            "prevencion": {"es": "Regla 20-20-20, pantalla a 50-70 cm, brillo adecuado", "kw": "20-20-20 kamachiyta katiy"},
        },
    },
    {
        "id": uuid.UUID("60000000-0000-0000-0000-000000000004"),
        "slug": "estres-laboral-docente",
        "categoria": "psicosocial",
        "codigo_cie10": "Z73.0",
        "esta_publicado": True,
        "traducciones": {
            "nombre": {"es": "EstrÃ©s Laboral Docente", "kw": "Yachachik llaki"},
            "descripcion": {"es": "Sindrome de agotamiento profesional en docentes por sobrecarga laboral", "kw": "Yachachikpak llaki"},
            "sintomas": {"es": "Agotamiento, irritabilidad, dificultad para concentrarse, insomnio", "kw": "Sayki, piÃ±ay, mana puÃ±uy"},
            "prevencion": {"es": "Tecnicas de relajacion, limites de trabajo, actividad fisica, apoyo social", "kw": "Samarina, kallpachina"},
        },
    },
]


class EnfermedadesOcupacionalesSeeder(BaseSeeder):
    """Seeder para catalogo de enfermedades ocupacionales."""

    async def seed(self) -> None:
        for datos in ENFERMEDADES:
            traducciones = datos.pop("traducciones")

            if await self.existe(EnfermedadOcupacional, slug=datos["slug"]):
                self.logger.info("enfermedad_omitida", slug=datos["slug"])
                self.omitidos += 1
                datos["traducciones"] = traducciones
                continue

            enfermedad = await self.insertar(EnfermedadOcupacional, datos)

            for campo, valores in traducciones.items():
                for codigo_idioma, valor in valores.items():
                    idioma_id = ID_IDIOMA_ES if codigo_idioma == "es" else ID_IDIOMA_KW
                    await self.insertar(Traduccion, {
                        "tabla": "enfermedades_ocupacionales",
                        "registro_id": enfermedad.id,
                        "campo": campo,
                        "idioma_id": idioma_id,
                        "valor": valor,
                    })

            datos["traducciones"] = traducciones
            self.logger.info("enfermedad_insertada", slug=datos["slug"])

        self.log_resumen()