"""
Datos iniciales: contenidos ergonomicos educativos con traducciones.
"""
import uuid
from app.models.contenidos_ergonomicos import ContenidoErgonomico
from app.models.traducciones import Traduccion
from seeders.base_seeder import BaseSeeder

ID_IDIOMA_ES = uuid.UUID("00000000-0000-0000-0000-000000000001")
ID_IDIOMA_KW = uuid.UUID("00000000-0000-0000-0000-000000000002")

CONTENIDOS = [
    {
        "id": uuid.UUID("50000000-0000-0000-0000-000000000001"),
        "slug": "ergonomia-basica-docentes",
        "tipo": "articulo",
        "nivel_dificultad": "basico",
        "tiempo_lectura_minutos": 5,
        "orden": 1,
        "esta_publicado": True,
        "esta_destacado": True,
        "vistas": 0,
        "traducciones": {
            "titulo": {"es": "ErgonomÃ­a BÃ¡sica para Docentes", "kw": "Allichishka tiyarina yachachikkunapak"},
            "descripcion": {"es": "Principios fundamentales de ergonomia aplicados al trabajo docente", "kw": "Yachachikkunapak allichishka llankay"},
            "contenido": {"es": "La ergonomia es la ciencia que estudia la relacion entre el ser humano y su entorno de trabajo...", "kw": "Allichishka llankay yachaypi..."},
        },
    },
    {
        "id": uuid.UUID("50000000-0000-0000-0000-000000000002"),
        "slug": "postura-correcta-escritorio",
        "tipo": "articulo",
        "nivel_dificultad": "basico",
        "tiempo_lectura_minutos": 4,
        "orden": 2,
        "esta_publicado": True,
        "esta_destacado": True,
        "vistas": 0,
        "traducciones": {
            "titulo": {"es": "Postura Correcta Frente al Escritorio", "kw": "Alli tiyarina"},
            "descripcion": {"es": "Guia practica para mantener una postura saludable durante el trabajo de oficina", "kw": "Alli tiyarina yachana"},
            "contenido": {"es": "Mantener una postura correcta es esencial para prevenir dolores crÃ³nicos...", "kw": "Alli tiyarispa llankay..."},
        },
    },
    {
        "id": uuid.UUID("50000000-0000-0000-0000-000000000003"),
        "slug": "sindrome-tunel-carpiano-prevencion",
        "tipo": "articulo",
        "nivel_dificultad": "intermedio",
        "tiempo_lectura_minutos": 7,
        "orden": 3,
        "esta_publicado": True,
        "esta_destacado": False,
        "vistas": 0,
        "traducciones": {
            "titulo": {"es": "PrevenciÃ³n del SÃ­ndrome del TÃºnel Carpiano", "kw": "Maki unchiymanta kacharishka"},
            "descripcion": {"es": "Como prevenir y tratar el sindrome del tunel carpiano en docentes", "kw": "Maki unchiyta anchuchina"},
            "contenido": {"es": "El sindrome del tunel carpiano es una de las lesiones mÃ¡s comunes en docentes...", "kw": "Maki unchiy yachachikkunapi..."},
        },
    },
]


class ContenidosErgonomicosSeeder(BaseSeeder):
    """Seeder para contenidos ergonomicos educativos."""

    async def seed(self) -> None:
        for datos in CONTENIDOS:
            traducciones = datos.pop("traducciones")

            if await self.existe(ContenidoErgonomico, slug=datos["slug"]):
                self.logger.info("contenido_omitido", slug=datos["slug"])
                self.omitidos += 1
                datos["traducciones"] = traducciones
                continue

            contenido = await self.insertar(ContenidoErgonomico, datos)

            for campo, valores in traducciones.items():
                for codigo_idioma, valor in valores.items():
                    idioma_id = ID_IDIOMA_ES if codigo_idioma == "es" else ID_IDIOMA_KW
                    await self.insertar(Traduccion, {
                        "tabla": "contenidos_ergonomicos",
                        "registro_id": contenido.id,
                        "campo": campo,
                        "idioma_id": idioma_id,
                        "valor": valor,
                    })

            datos["traducciones"] = traducciones
            self.logger.info("contenido_insertado", slug=datos["slug"])

        self.log_resumen()