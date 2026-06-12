"""
Importaciones centralizadas de todos los schemas.
"""
# Base
from app.schemas.base import (
    PaginationQuerySchema,
    PaginationResponseSchema,
    RespuestaExitosaSchema,
    RespuestaErrorSchema,
    # Enums
    RolEnum,
    PlataformaEnum,
    NivelExperienciaEnum,
    TemaEnum,
    TipoRecursoEnum,
    NivelDificultadEnum,
    TipoActividadEnum,
    TipoRecordatorioEnum,
    AccionAuditoriaEnum,
)

# Usuarios
from app.schemas.usuarios_schemas import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuariosListResponse,
)

# Dispositivos
from app.schemas.dispositivos_schemas import (
    DispositivoRegisterSchema,
    DispositivoUpdateSchema,
    DispositivoResponse,
    DispositivosListResponse,
)

# Idiomas
from app.schemas.idiomas_schemas import (
    IdiomaResponse,
    IdiomasListResponse,
)

# Traducciones
from app.schemas.traducciones_schemas import (
    TraduccionCreateSchema,
    TraduccionUpdateSchema,
    TraduccionResponse,
    TraduccionesListResponse,
)

# Preferencias
from app.schemas.preferencias_usuario_schemas import (
    PreferenciasUsuarioResponse,
    PreferenciasUsuarioUpdateSchema,
)

# Archivos Media
from app.schemas.archivos_media_schemas import (
    ArchivoMediaUploadSchema,
    ArchivoMediaResponse,
    ArchivosMediaListResponse,
)

# Categorías Ejercicios
from app.schemas.categorias_ejercicios_schemas import (
    CategoriaEjercicioResponse,
    CategoriasEjerciciosListResponse,
)

# Emociones
from app.schemas.emociones_schemas import (
    EmocionResponse,
    EmocionesListResponse,
)

# Contenidos Ergonómicos
from app.schemas.contenidos_ergonomicos_schemas import (
    ContenidoErgonomicoResponse,
    ContenidosErgonomicosListResponse,
)

# Enfermedades Ocupacionales
from app.schemas.enfermedades_ocupacionales_schemas import (
    EnfermedadOcupacionalResponse,
    EnfermedadesOcupacionalesListResponse,
)

# Ejercicios
from app.schemas.ejercicios_schemas import (
    CategoriaEjercicioMini,
    EjercicioResponse,
    EjerciciosListResponse,
)

# Rutinas
from app.schemas.rutinas_pausas_activas_schemas import (
    RutinaPausaActivaResponse,
    RutinasListResponse,
)

# Ejercicios Rutina
from app.schemas.ejercicios_rutina_schemas import (
    EjercicioRutinaResponse,
    EjercicioRutinaListResponse,
)

# Progreso Usuario
from app.schemas.progreso_usuario_schemas import (
    ProgresoUsuarioCreateSchema,
    ProgresoUsuarioResponse,
    ProgresoUsuarioListResponse,
)

# Recordatorios
from app.schemas.recordatorios_schemas import (
    RecordatorioCreateSchema,
    RecordatorioUpdateSchema,
    RecordatorioResponse,
    RecordatoriosListResponse,
)

# Registros Emocionales
from app.schemas.registros_emocionales_schemas import (
    RegistroEmocionalCreateSchema,
    RegistroEmocionalResponse,
    RegistrosEmocionalListResponse,
)

# Recomendaciones Emocionales
from app.schemas.recomendaciones_emocionales_schemas import (
    RecomendacionEmocionalCreateSchema,
    RecomendacionEmocionalResponse,
    RecomendacionesEmocionalListResponse,
)

# Consejos
from app.schemas.consejos_schemas import (
    ConsejoResponse,
    ConsejosListResponse,
)

# Mensajes Motivacionales
from app.schemas.mensajes_motivacionales_schemas import (
    MensajeMotivacionalResponse,
    MensajesMotivacionalesListResponse,
)

# Auditoría
from app.schemas.registros_auditoria_schemas import (
    RegistroAuditoriaResponse,
    RegistrosAuditoriaListResponse,
)

__all__ = [
    # Base & Pagination
    "PaginationQuerySchema",
    "PaginationResponseSchema",
    "RespuestaExitosaSchema",
    "RespuestaErrorSchema",
    # Enums
    "RolEnum",
    "PlataformaEnum",
    "NivelExperienciaEnum",
    "TemaEnum",
    "TipoRecursoEnum",
    "NivelDificultadEnum",
    "TipoActividadEnum",
    "TipoRecordatorioEnum",
    "AccionAuditoriaEnum",
    # Usuarios
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    "UsuariosListResponse",
    # Dispositivos
    "DispositivoRegisterSchema",
    "DispositivoUpdateSchema",
    "DispositivoResponse",
    "DispositivosListResponse",
    # Idiomas
    "IdiomaResponse",
    "IdiomasListResponse",
    # Traducciones
    "TraduccionCreateSchema",
    "TraduccionUpdateSchema",
    "TraduccionResponse",
    "TraduccionesListResponse",
    # Preferencias
    "PreferenciasUsuarioResponse",
    "PreferenciasUsuarioUpdateSchema",
    # Archivos Media
    "ArchivoMediaUploadSchema",
    "ArchivoMediaResponse",
    "ArchivosMediaListResponse",
    # Categorías Ejercicios
    "CategoriaEjercicioResponse",
    "CategoriasEjerciciosListResponse",
    # Emociones
    "EmocionResponse",
    "EmocionesListResponse",
    # Contenidos Ergonómicos
    "ContenidoErgonomicoResponse",
    "ContenidosErgonomicosListResponse",
    # Enfermedades Ocupacionales
    "EnfermedadOcupacionalResponse",
    "EnfermedadesOcupacionalesListResponse",
    # Ejercicios
    "CategoriaEjercicioMini",
    "EjercicioResponse",
    "EjerciciosListResponse",
    # Rutinas
    "RutinaPausaActivaResponse",
    "RutinasListResponse",
    # Ejercicios Rutina
    "EjercicioRutinaResponse",
    "EjercicioRutinaListResponse",
    # Progreso Usuario
    "ProgresoUsuarioCreateSchema",
    "ProgresoUsuarioResponse",
    "ProgresoUsuarioListResponse",
    # Recordatorios
    "RecordatorioCreateSchema",
    "RecordatorioUpdateSchema",
    "RecordatorioResponse",
    "RecordatoriosListResponse",
    # Registros Emocionales
    "RegistroEmocionalCreateSchema",
    "RegistroEmocionalResponse",
    "RegistrosEmocionalListResponse",
    # Recomendaciones Emocionales
    "RecomendacionEmocionalCreateSchema",
    "RecomendacionEmocionalResponse",
    "RecomendacionesEmocionalListResponse",
    # Consejos
    "ConsejoResponse",
    "ConsejosListResponse",
    # Mensajes Motivacionales
    "MensajeMotivacionalResponse",
    "MensajesMotivacionalesListResponse",
    # Auditoría
    "RegistroAuditoriaResponse",
    "RegistrosAuditoriaListResponse",
]