"""
Importación centralizada de todos los modelos SQLAlchemy.
Alembic detecta los modelos importados aquí.
"""
from app.models.base import Base, ModeloBase, ModeloConEliminacion, ModeloTranslatable

# ── Catálogos ──────────────────────────────────────────────────────────────────
from app.models.usuarios import Usuario
from app.models.dispositivos import Dispositivo
from app.models.idiomas import Idioma
from app.models.traducciones import Traduccion
from app.models.categorias_ejercicios import CategoriaEjercicio
from app.models.emociones import Emocion

# ── Contenido educativo ────────────────────────────────────────────────────────
from app.models.contenidos_ergonomicos import ContenidoErgonomico
from app.models.enfermedades_ocupacionales import EnfermedadOcupacional
from app.models.consejos import Consejo
from app.models.mensajes_motivacionales import MensajeMotivacional

# ── Ejercicios y rutinas ──────────────────────────────────────────────────────
from app.models.ejercicios import Ejercicio
from app.models.rutinas_pausas_activas import RutinaPausaActiva
from app.models.ejercicios_rutina import EjercicioRutina

# ── Datos del usuario (por dispositivo) ────────────────────────────────────────
from app.models.preferencias_usuario import PreferenciasUsuario
from app.models.progreso_usuario import ProgresoUsuario
from app.models.recordatorios import Recordatorio
from app.models.registros_emocionales import RegistroEmocional
from app.models.recomendaciones_emocionales import RecomendacionEmocional

# ── Media ──────────────────────────────────────────────────────────────────────
from app.models.archivos_media import ArchivoMedia

# ── Auditoría ──────────────────────────────────────────────────────────────────
from app.models.registros_auditoria import RegistroAuditoria

__all__ = [
    # Base
    "Base",
    "ModeloBase",
    "ModeloConEliminacion",
    "ModeloTranslatable",
    # Usuarios y dispositivos
    "Usuario",
    "Dispositivo",
    # Idiomas y traducciones
    "Idioma",
    "Traduccion",
    # Contenido educativo
    "ContenidoErgonomico",
    "EnfermedadOcupacional",
    "Consejo",
    "MensajeMotivacional",
    # Ejercicios y rutinas
    "CategoriaEjercicio",
    "Ejercicio",
    "RutinaPausaActiva",
    "EjercicioRutina",
    # Datos del usuario
    "PreferenciasUsuario",
    "ProgresoUsuario",
    "Recordatorio",
    "RegistroEmocional",
    "RecomendacionEmocional",
    "Emocion",
    # Media
    "ArchivoMedia",
    # Auditoría
    "RegistroAuditoria",
]