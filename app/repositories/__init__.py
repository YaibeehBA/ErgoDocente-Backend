"""
Importaciones centralizadas de todos los repositories.
"""
from app.repositories.base import BaseRepository
from app.repositories.usuarios_repository import UsuarioRepository
from app.repositories.dispositivos_repository import DispositivoRepository
from app.repositories.idiomas_repository import IdiomaRepository
from app.repositories.traducciones_repository import TraduccionRepository
from app.repositories.preferencias_usuario_repository import PreferenciasUsuarioRepository
from app.repositories.archivos_media_repository import ArchivoMediaRepository
from app.repositories.contenidos_ergonomicos_repository import ContenidoErgonomicoRepository
from app.repositories.enfermedades_ocupacionales_repository import EnfermedadOcupacionalRepository
from app.repositories.categorias_ejercicios_repository import CategoriaEjercicioRepository
from app.repositories.ejercicios_repository import EjercicioRepository
from app.repositories.rutinas_pausas_activas_repository import RutinaPausaActivaRepository
from app.repositories.ejercicios_rutina_repository import EjercicioRutinaRepository
from app.repositories.progreso_usuario_repository import ProgresoUsuarioRepository
from app.repositories.recordatorios_repository import RecordatorioRepository
from app.repositories.emociones_repository import EmocionRepository
from app.repositories.registros_emocionales_repository import RegistroEmocionalRepository
from app.repositories.recomendaciones_emocionales_repository import RecomendacionEmocionalRepository
from app.repositories.consejos_repository import ConsejoRepository
from app.repositories.mensajes_motivacionales_repository import MensajeMotivacionalRepository
from app.repositories.registros_auditoria_repository import RegistroAuditoriaRepository

__all__ = [
    "BaseRepository",
    "UsuarioRepository",
    "DispositivoRepository",
    "IdiomaRepository",
    "TraduccionRepository",
    "PreferenciasUsuarioRepository",
    "ArchivoMediaRepository",
    "ContenidoErgonomicoRepository",
    "EnfermedadOcupacionalRepository",
    "CategoriaEjercicioRepository",
    "EjercicioRepository",
    "RutinaPausaActivaRepository",
    "EjercicioRutinaRepository",
    "ProgresoUsuarioRepository",
    "RecordatorioRepository",
    "EmocionRepository",
    "RegistroEmocionalRepository",
    "RecomendacionEmocionalRepository",
    "ConsejoRepository",
    "MensajeMotivacionalRepository",
    "RegistroAuditoriaRepository",
]