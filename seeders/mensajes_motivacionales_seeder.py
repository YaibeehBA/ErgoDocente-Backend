"""
Datos iniciales: mensajes motivacionales con traducciones.
"""
import uuid
from app.models.mensajes_motivacionales import MensajeMotivacional
from app.models.traducciones import Traduccion
from seeders.base_seeder import BaseSeeder

ID_IDIOMA_ES = uuid.UUID("00000000-0000-0000-0000-000000000001")
ID_IDIOMA_KW = uuid.UUID("00000000-0000-0000-0000-000000000002")

MENSAJES = [
    {
        "id": uuid.UUID("80000000-0000-0000-0000-000000000001"),
        "autor": "AnÃ³nimo",
        "categoria": "motivacion",
        "esta_publicado": True,
        "traducciones": {
            "texto": {"es": "Cada pausa activa es una inversiÃ³n en tu salud y productividad.", "kw": "Samarichina kallpanata kutin kuna"},
        },
    },
    {
        "id": uuid.UUID("80000000-0000-0000-0000-000000000002"),
        "autor": "AnÃ³nimo",
        "categoria": "bienestar",
        "esta_publicado": True,
        "traducciones": {
            "texto": {"es": "Tu cuerpo es el instrumento de tu trabajo. CuÃ­dalo.", "kw": "Kuerpota wankana shinami, alli kawachiy"},
        },
    },
    {
        "id": uuid.UUID("80000000-0000-0000-0000-000000000003"),
        "autor": "HipÃ³crates",
        "categoria": "salud",
        "esta_publicado": True,
        "traducciones": {
            "texto": {"es": "Que tu medicina sea tu alimento y tu alimento sea tu medicina.", "kw": "Mikhuna mikunami hampi kana"},
        },
    },
    {
        "id": uuid.UUID("80000000-0000-0000-0000-000000000004"),
        "autor": "AnÃ³nimo",
        "categoria": "ergonomia",
        "esta_publicado": True,
        "traducciones": {
            "texto": {"es": "Cinco minutos de movimiento pueden transformar tu jornada laboral.", "kw": "Pichka minutopi muyuna llankayta allichin"},
        },
    },
    {
        "id": uuid.UUID("80000000-0000-0000-0000-000000000005"),
        "autor": "AnÃ³nimo",
        "categoria": "motivacion",
        "esta_publicado": True,
        "traducciones": {
            "texto": {"es": "Un docente saludable inspira a sus estudiantes con energÃ­a y pasiÃ³n.", "kw": "Alli yachachik sumakta yachachin"},
        },
    },
    {
        "id": uuid.UUID("80000000-0000-0000-0000-000000000006"),
        "autor": "AnÃ³nimo",
        "categoria": "bienestar",
        "esta_publicado": True,
        "traducciones": {
            "texto": {"es": "Respira profundo. Tu siguiente clase serÃ¡ mejor.", "kw": "Sumakta samay. Katik yachachina alli kanka"},
        },
    },
]


class MensajesMotivacionalesSeeder(BaseSeeder):
    """Seeder para mensajes motivacionales."""

    async def seed(self) -> None:
        for datos in MENSAJES:
            traducciones = datos.pop("traducciones")

            if await self.existe(MensajeMotivacional, id=datos["id"]):
                self.logger.info("mensaje_omitido", id=str(datos["id"])[:8])
                self.omitidos += 1
                datos["traducciones"] = traducciones
                continue

            mensaje = await self.insertar(MensajeMotivacional, datos)

            for campo, valores in traducciones.items():
                for codigo_idioma, valor in valores.items():
                    idioma_id = ID_IDIOMA_ES if codigo_idioma == "es" else ID_IDIOMA_KW
                    await self.insertar(Traduccion, {
                        "tabla": "mensajes_motivacionales",
                        "registro_id": mensaje.id,
                        "campo": campo,
                        "idioma_id": idioma_id,
                        "valor": valor,
                    })

            datos["traducciones"] = traducciones
            self.logger.info("mensaje_insertado", autor=datos.get("autor"))

        self.log_resumen()