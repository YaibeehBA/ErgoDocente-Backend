"""
Logica de negocio para RegistroEmocional.
Incluye logica de recomendaciones basada en estado emocional.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.registros_emocionales_repository import RegistroEmocionalRepository
from app.repositories.recomendaciones_emocionales_repository import RecomendacionEmocionalRepository
from app.services.base import BaseService


class RegistroEmocionalService(BaseService):
    """Service para tracking emocional y recomendaciones automaticas."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        from app.models.registros_emocionales import RegistroEmocional
        from app.models.recomendaciones_emocionales import RecomendacionEmocional
        self.repo = RegistroEmocionalRepository(db, RegistroEmocional)
        self.repo_recomendaciones = RecomendacionEmocionalRepository(db, RecomendacionEmocional)

    async def registrar(self, dispositivo_id: UUID, datos: dict):
        """
        Registrar estado emocional del usuario.
        Retorna el registro + recomendaciones automaticas.
        """
        datos["dispositivo_id"] = dispositivo_id
        registro = await self.repo.crear(datos)
        await self.commit()

        self.logger.info(
            "emocion_registrada",
            dispositivo_id=str(dispositivo_id),
            emocion_id=str(datos.get("emocion_id")),
            intensidad=datos.get("intensidad"),
        )
        return registro

    
    async def obtener_recomendaciones_para_registro(self, registro_id: UUID) -> list:
        """
        Obtener recomendaciones basadas en el registro emocional.
        Busca recomendaciones asociadas a la emocion del registro.
        """
        registro = await self.repo.obtener_o_error(registro_id)
        return await self.repo_recomendaciones.obtener_recomendaciones_emocion(
            registro.emocion_id
        )
        

    async def listar_por_dispositivo(self, dispositivo_id: UUID, page: int = 1, page_size: int = 20):
        """Listar registros emocionales de un dispositivo."""
        return await self.repo.listar_por_dispositivo(dispositivo_id, page, page_size)

    async def listar_ultimas_24h(self, dispositivo_id: UUID):
        """Listar registros de las ultimas 24 horas."""
        return await self.repo.listar_ultimas_horas(dispositivo_id, horas=24)

    async def obtener_estadisticas(self, dispositivo_id: UUID) -> dict:
        """
        Resumen emocional del dispositivo en las ultimas 24h.
        Retorna conteos y emocion predominante.
        """
        registros = await self.repo.listar_ultimas_horas(dispositivo_id, horas=24)
        if not registros:
            return {"total_registros": 0, "emocion_predominante": None}

        conteo: dict[str, int] = {}
        for r in registros:
            key = str(r.emocion_id)
            conteo[key] = conteo.get(key, 0) + 1

        emocion_predominante = max(conteo, key=lambda k: conteo[k])
        return {
            "total_registros": len(registros),
            "emocion_predominante_id": emocion_predominante,
            "conteo_por_emocion": conteo,
        }