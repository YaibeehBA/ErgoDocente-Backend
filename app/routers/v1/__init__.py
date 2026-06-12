"""
Importaciones de todos los routers v1.
"""
from app.routers.v1 import (
    dispositivos_router,
    idiomas_router,
    preferencias_usuario_router,
    ejercicios_router,
    rutinas_router,
    emociones_router,
    registros_emocionales_router,
    progreso_router,
    recordatorios_router,
    categorias_router,
    contenidos_router,
    enfermedades_router,
    consejos_router,
    mensajes_router,
    archivos_media_router,
    health_router,
)

routers = [
    health_router.router,
    dispositivos_router.router,
    idiomas_router.router,
    preferencias_usuario_router.router,
    ejercicios_router.router,
    rutinas_router.router,
    emociones_router.router,
    registros_emocionales_router.router,
    progreso_router.router,
    recordatorios_router.router,
    categorias_router.router,
    contenidos_router.router,
    enfermedades_router.router,
    consejos_router.router,
    mensajes_router.router,
    archivos_media_router.router,
]

__all__ = ["routers"]