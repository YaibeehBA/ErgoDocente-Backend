"""
Datos iniciales: idiomas disponibles (Espanol y Kichwa).
"""
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.idiomas import Idioma
from seeders.base_seeder import BaseSeeder

IDIOMAS = [
    {
        "id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
        "codigo": "es",
        "nombre": "EspaÃ±ol",
        "nombre_en_espanol": "EspaÃ±ol",
        "direccion_texto": "ltr",
        "bandera_emoji": "ðŸ‡ªðŸ‡¸",
        "es_predeterminado": True,
        "esta_activo": True,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0000-000000000002"),
        "codigo": "kw",
        "nombre": "Kichwa",
        "nombre_en_espanol": "Kichwa",
        "direccion_texto": "ltr",
        "bandera_emoji": "ðŸ‡ªðŸ‡¨",
        "es_predeterminado": False,
        "esta_activo": True,
    },
]


class IdiomasSeeder(BaseSeeder):
    """Seeder para idiomas disponibles."""

    async def seed(self) -> None:
        """Insertar idiomas si no existen."""
        for datos in IDIOMAS:
            if await self.existe(Idioma, codigo=datos["codigo"]):
                self.logger.info("idioma_omitido", codigo=datos["codigo"])
                self.omitidos += 1
                continue
            await self.insertar(Idioma, datos)
            self.logger.info("idioma_insertado", codigo=datos["codigo"])

        self.log_resumen()