"""
Datos iniciales: ejercicios de pausa activa con traducciones.
"""
import uuid
from app.models.ejercicios import Ejercicio
from app.models.traducciones import Traduccion
from seeders.base_seeder import BaseSeeder

ID_IDIOMA_ES = uuid.UUID("00000000-0000-0000-0000-000000000001")
ID_IDIOMA_KW = uuid.UUID("00000000-0000-0000-0000-000000000002")

# IDs de categorias (deben coincidir con categorias_ejercicios_seeder.py)
CAT_CUELLO    = uuid.UUID("20000000-0000-0000-0000-000000000001")
CAT_ESPALDA   = uuid.UUID("20000000-0000-0000-0000-000000000002")
CAT_MUNECAS   = uuid.UUID("20000000-0000-0000-0000-000000000003")
CAT_OJOS      = uuid.UUID("20000000-0000-0000-0000-000000000004")
CAT_RESP      = uuid.UUID("20000000-0000-0000-0000-000000000005")
CAT_PIERNAS   = uuid.UUID("20000000-0000-0000-0000-000000000006")

EJERCICIOS = [
    {
        "id": uuid.UUID("30000000-0000-0000-0000-000000000001"),
        "slug": "rotacion-cuello",
        "categoria_id": CAT_CUELLO,
        "duracion_segundos": 60,
        "repeticiones": 5,
        "series": 1,
        "nivel_dificultad": "principiante",
        "parte_cuerpo": "cuello",
        "posicion_inicial": "sentado",
        "requiere_material": False,
        "esta_publicado": True,
        "esta_destacado": True,
        "traducciones": {
            "titulo": {"es": "RotaciÃ³n de Cuello", "kw": "Kunka muyuchina"},
            "descripcion": {"es": "Gira suavemente la cabeza de lado a lado para aliviar tension", "kw": "Kunkata sumakta muyuchi"},
            "instrucciones": {"es": "Inclina la cabeza hacia la derecha, sostÃ©n 5 segundos, repite al lado izquierdo", "kw": "Kunkata pakayman churay, 5 segundota charin"},
        },
    },
    {
        "id": uuid.UUID("30000000-0000-0000-0000-000000000002"),
        "slug": "estiramiento-hombros",
        "categoria_id": CAT_CUELLO,
        "duracion_segundos": 45,
        "repeticiones": 3,
        "series": 2,
        "nivel_dificultad": "principiante",
        "parte_cuerpo": "hombros",
        "posicion_inicial": "sentado o de pie",
        "requiere_material": False,
        "esta_publicado": True,
        "esta_destacado": False,
        "traducciones": {
            "titulo": {"es": "Estiramiento de Hombros", "kw": "Rikra shuyuchina"},
            "descripcion": {"es": "Estira los musculos del hombro para liberar tension acumulada", "kw": "Rikrata kallpachina"},
            "instrucciones": {"es": "Lleva el brazo derecho al pecho, sostÃ©n con el brazo izquierdo 15 segundos", "kw": "Pakayman maquita apay"},
        },
    },
    {
        "id": uuid.UUID("30000000-0000-0000-0000-000000000003"),
        "slug": "estiramiento-espalda-baja",
        "categoria_id": CAT_ESPALDA,
        "duracion_segundos": 60,
        "repeticiones": 3,
        "series": 1,
        "nivel_dificultad": "principiante",
        "parte_cuerpo": "espalda baja",
        "posicion_inicial": "sentado",
        "requiere_material": False,
        "esta_publicado": True,
        "esta_destacado": True,
        "traducciones": {
            "titulo": {"es": "Estiramiento de Espalda Baja", "kw": "Ura wasa shuyuchina"},
            "descripcion": {"es": "Alivia la tension lumbar causada por largas horas sentado", "kw": "Ura wasat samarichina"},
            "instrucciones": {"es": "Inclinate hacia adelante desde la silla, deja caer los brazos hacia el suelo por 20 segundos", "kw": "Ã‘awpaman urmarichiy"},
        },
    },
    {
        "id": uuid.UUID("30000000-0000-0000-0000-000000000004"),
        "slug": "flexion-munecas",
        "categoria_id": CAT_MUNECAS,
        "duracion_segundos": 30,
        "repeticiones": 10,
        "series": 2,
        "nivel_dificultad": "principiante",
        "parte_cuerpo": "muÃ±ecas",
        "posicion_inicial": "sentado",
        "requiere_material": False,
        "esta_publicado": True,
        "esta_destacado": False,
        "traducciones": {
            "titulo": {"es": "FlexiÃ³n de MuÃ±ecas", "kw": "Maki muyuchina"},
            "descripcion": {"es": "Ejercicio para prevenir el sindrome del tunel carpiano", "kw": "Maki wanuchina"},
            "instrucciones": {"es": "Extiende la mano hacia arriba y hacia abajo lentamente 10 veces", "kw": "Makita hawaman, uramanta muyuchi"},
        },
    },
    {
        "id": uuid.UUID("30000000-0000-0000-0000-000000000005"),
        "slug": "descanso-visual-20-20-20",
        "categoria_id": CAT_OJOS,
        "duracion_segundos": 20,
        "repeticiones": 1,
        "series": 1,
        "nivel_dificultad": "principiante",
        "parte_cuerpo": "ojos",
        "posicion_inicial": "sentado",
        "requiere_material": False,
        "esta_publicado": True,
        "esta_destacado": True,
        "traducciones": {
            "titulo": {"es": "Regla 20-20-20 para los Ojos", "kw": "Ã‘awi samarichina"},
            "descripcion": {"es": "Cada 20 minutos mira algo a 20 pies por 20 segundos", "kw": "Ã‘awita karu llaktaman chaway"},
            "instrucciones": {"es": "Mira un objeto a 6 metros de distancia durante 20 segundos sin parpadear", "kw": "Karupi tiyak imata 20 segundota ricuy"},
        },
    },
    {
        "id": uuid.UUID("30000000-0000-0000-0000-000000000006"),
        "slug": "respiracion-diafragmatica",
        "categoria_id": CAT_RESP,
        "duracion_segundos": 120,
        "repeticiones": 5,
        "series": 1,
        "nivel_dificultad": "principiante",
        "parte_cuerpo": "torso",
        "posicion_inicial": "sentado o recostado",
        "requiere_material": False,
        "esta_publicado": True,
        "esta_destacado": True,
        "traducciones": {
            "titulo": {"es": "RespiraciÃ³n DiafragmÃ¡tica", "kw": "Sumak samay"},
            "descripcion": {"es": "Tecnica de respiracion profunda para reducir estres y ansiedad", "kw": "Alli samayta yachana"},
            "instrucciones": {"es": "Inhala 4 segundos por la nariz, sostÃ©n 4 segundos, exhala 6 segundos por la boca", "kw": "Shinarinata 4 segundo ukhuman, 4 segundo charin, 6 segundo llukshichiy"},
        },
    },
    {
        "id": uuid.UUID("30000000-0000-0000-0000-000000000007"),
        "slug": "elevacion-talones",
        "categoria_id": CAT_PIERNAS,
        "duracion_segundos": 60,
        "repeticiones": 15,
        "series": 2,
        "nivel_dificultad": "principiante",
        "parte_cuerpo": "piernas",
        "posicion_inicial": "de pie",
        "requiere_material": False,
        "esta_publicado": True,
        "esta_destacado": False,
        "traducciones": {
            "titulo": {"es": "ElevaciÃ³n de Talones", "kw": "Chaki hawaman churana"},
            "descripcion": {"es": "Activa la circulacion sanguinea en piernas y pies", "kw": "Chakipi yawar kawsachina"},
            "instrucciones": {"es": "De pie, eleva los talones del suelo lentamente y baja. Repite 15 veces", "kw": "Chakikunata hawaman churay, uramanta urmarichiy"},
        },
    },
]


class EjerciciosSeeder(BaseSeeder):
    """Seeder para ejercicios con traducciones."""

    async def seed(self) -> None:
        for datos in EJERCICIOS:
            traducciones = datos.pop("traducciones")

            if await self.existe(Ejercicio, slug=datos["slug"]):
                self.logger.info("ejercicio_omitido", slug=datos["slug"])
                self.omitidos += 1
                datos["traducciones"] = traducciones
                continue

            ejercicio = await self.insertar(Ejercicio, datos)

            for campo, valores in traducciones.items():
                for codigo_idioma, valor in valores.items():
                    idioma_id = ID_IDIOMA_ES if codigo_idioma == "es" else ID_IDIOMA_KW
                    await self.insertar(Traduccion, {
                        "tabla": "ejercicios",
                        "registro_id": ejercicio.id,
                        "campo": campo,
                        "idioma_id": idioma_id,
                        "valor": valor,
                    })

            datos["traducciones"] = traducciones
            self.logger.info("ejercicio_insertado", slug=datos["slug"])

        self.log_resumen()