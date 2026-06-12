"""
Migración inicial: crear todas las tablas, índices y constrains.
Generada con: alembic revision --autogenerate -m "initial schema"
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '001_20250101_000000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crear todas las tablas en la base de datos."""

    # Tabla: idiomas
    op.create_table(
        'idiomas',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('codigo', sa.String(10), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('nombre_en_espanol', sa.String(100), nullable=False),
        sa.Column('direccion_texto', sa.String(3), server_default='ltr', nullable=False),
        sa.Column('bandera_emoji', sa.String(10), nullable=True),
        sa.Column('es_predeterminado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('esta_activo', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo'),
    )
    op.create_index('ix_idiomas_codigo', 'idiomas', ['codigo'])
    op.create_index('ix_idiomas_id', 'idiomas', ['id'])

    # Tabla: usuarios
    op.create_table(
        'usuarios',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('correo', sa.String(255), nullable=False),
        sa.Column('nombre_completo', sa.String(255), nullable=False),
        sa.Column('nombre_usuario', sa.String(100), nullable=True),
        sa.Column('telefono', sa.String(20), nullable=True),
        sa.Column('foto_perfil_url', sa.Text(), nullable=True),
        sa.Column('password_hash', sa.String(255), nullable=True),
        sa.Column('rol', sa.Enum('admin', 'usuario', name='rol_usuario_enum'), server_default='usuario', nullable=False),
        sa.Column('esta_activo', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('verificado_en', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ultimo_login_en', sa.DateTime(timezone=True), nullable=True),
        sa.Column('token_reset_password', sa.String(512), nullable=True),
        sa.Column('token_reset_expira_en', sa.DateTime(timezone=True), nullable=True),
        sa.Column('proveedor_oauth', sa.String(50), nullable=True),
        sa.Column('id_oauth', sa.String(255), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('correo'),
        sa.UniqueConstraint('nombre_usuario'),
    )
    op.create_index('ix_usuarios_correo', 'usuarios', ['correo'])
    op.create_index('ix_usuarios_id', 'usuarios', ['id'])
    op.create_index('ix_usuarios_nombre_usuario', 'usuarios', ['nombre_usuario'])
    op.create_index('ix_usuarios_eliminado_en', 'usuarios', ['eliminado_en'])

    # Tabla: archivos_media
    op.create_table(
        'archivos_media',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('public_id_cloudinary', sa.String(500), nullable=False),
        sa.Column('url_publica', sa.Text(), nullable=False),
        sa.Column('url_segura', sa.Text(), nullable=False),
        sa.Column('carpeta_cloudinary', sa.String(255), nullable=True),
        sa.Column('tipo_recurso', sa.Enum('imagen', 'video', 'audio', 'documento', name='tipo_recurso_enum'), nullable=False),
        sa.Column('formato', sa.String(20), nullable=True),
        sa.Column('tamano_bytes', sa.Integer(), nullable=True),
        sa.Column('ancho_px', sa.Integer(), nullable=True),
        sa.Column('alto_px', sa.Integer(), nullable=True),
        sa.Column('duracion_segundos', sa.Float(), nullable=True),
        sa.Column('nombre_original', sa.String(255), nullable=True),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('texto_alternativo', sa.String(500), nullable=True),
        sa.Column('esta_activo', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('dispositivo_subida_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('public_id_cloudinary'),
    )
    op.create_index('ix_archivos_media_id', 'archivos_media', ['id'])
    op.create_index('ix_archivos_media_public_id', 'archivos_media', ['public_id_cloudinary'])
    op.create_index('ix_archivos_media_tipo', 'archivos_media', ['tipo_recurso'])
    op.create_index('ix_archivos_media_dispositivo', 'archivos_media', ['dispositivo_subida_id'])

   # Tabla: dispositivos
    op.create_table(
        'dispositivos',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('identificador_dispositivo', sa.String(255), nullable=False),
        sa.Column('nombre_dispositivo', sa.String(255), nullable=True),
        sa.Column('plataforma', sa.String(20), nullable=True),
        sa.Column('modelo_dispositivo', sa.String(100), nullable=True),
        sa.Column('version_so', sa.String(50), nullable=True),
        sa.Column('version_app', sa.String(20), nullable=True),
        sa.Column('token_notificacion', sa.Text(), nullable=True),
        sa.Column('esta_activo', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('ultimo_acceso', sa.DateTime(timezone=True), nullable=True),  
        sa.Column('usuario_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('identificador_dispositivo'),
    )

    # Tabla: preferencias_usuario
    op.create_table(
        'preferencias_usuario',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dispositivo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('idioma_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('notificaciones_habilitadas', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('frecuencia_recordatorio_minutos', sa.Integer(), server_default='60', nullable=False),
        sa.Column('hora_inicio_trabajo', sa.Time(), nullable=True),
        sa.Column('hora_fin_trabajo', sa.Time(), nullable=True),
        sa.Column('nivel_experiencia', sa.Enum('principiante', 'intermedio', 'avanzado', name='nivel_experiencia_enum'), server_default='principiante', nullable=False),
        sa.Column('objetivo_principal', sa.String(255), nullable=True),
        sa.Column('condicion_fisica', sa.Text(), nullable=True),
        sa.Column('tema', sa.Enum('claro', 'oscuro', 'sistema', name='tema_enum'), server_default='sistema', nullable=False),
        sa.Column('sonido_habilitado', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['dispositivo_id'], ['dispositivos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['idioma_id'], ['idiomas.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dispositivo_id', name='uq_preferencias_dispositivo'),
    )
    op.create_index('ix_preferencias_dispositivo_id', 'preferencias_usuario', ['dispositivo_id'])
    op.create_index('ix_preferencias_idioma_id', 'preferencias_usuario', ['idioma_id'])

    # Tabla: traducciones
    op.create_table(
        'traducciones',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tabla', sa.String(100), nullable=False),
        sa.Column('registro_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('campo', sa.String(100), nullable=False),
        sa.Column('idioma_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('valor', sa.Text(), nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['idioma_id'], ['idiomas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tabla', 'registro_id', 'campo', 'idioma_id', name='uq_traduccion_tabla_registro_campo_idioma'),
    )
    op.create_index('ix_traducciones_id', 'traducciones', ['id'])
    op.create_index('ix_traducciones_tabla', 'traducciones', ['tabla'])
    op.create_index('ix_traducciones_registro', 'traducciones', ['registro_id'])
    op.create_index('ix_traducciones_idioma', 'traducciones', ['idioma_id'])

    # Tabla: categorias_ejercicios
    op.create_table(
        'categorias_ejercicios',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.Column('icono_url', sa.String(500), nullable=True),
        sa.Column('color_hex', sa.String(7), nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False),
        sa.Column('esta_activo', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('ix_categorias_id', 'categorias_ejercicios', ['id'])
    op.create_index('ix_categorias_slug', 'categorias_ejercicios', ['slug'])

    # Tabla: emociones
    op.create_table(
        'emociones',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.Column('emoji', sa.String(10), nullable=False),
        sa.Column('color_hex', sa.String(7), nullable=False),
        sa.Column('nivel_intensidad', sa.Integer(), nullable=False),
        sa.Column('es_positiva', sa.Boolean(), nullable=False),
        sa.Column('esta_activo', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('ix_emociones_id', 'emociones', ['id'])
    op.create_index('ix_emociones_slug', 'emociones', ['slug'])

    # Tabla: contenidos_ergonomicos
    op.create_table(
        'contenidos_ergonomicos',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('tipo', sa.Enum('articulo', 'video', 'infografia', 'audio', name='tipo_contenido_enum'), nullable=False),
        sa.Column('nivel_dificultad', sa.Enum('basico', 'intermedio', 'avanzado', name='nivel_dificultad_contenido_enum'), nullable=False),
        sa.Column('tiempo_lectura_minutos', sa.Integer(), nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False),
        sa.Column('esta_publicado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('esta_destacado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('vistas', sa.Integer(), server_default='0', nullable=False),
        sa.Column('archivo_media_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['archivo_media_id'], ['archivos_media.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('ix_contenidos_id', 'contenidos_ergonomicos', ['id'])
    op.create_index('ix_contenidos_slug', 'contenidos_ergonomicos', ['slug'])
    op.create_index('ix_contenidos_tipo', 'contenidos_ergonomicos', ['tipo'])
    op.create_index('ix_contenidos_publicado', 'contenidos_ergonomicos', ['esta_publicado'])
    op.create_index('ix_contenidos_eliminado', 'contenidos_ergonomicos', ['eliminado_en'])

    # Tabla: enfermedades_ocupacionales
    op.create_table(
        'enfermedades_ocupacionales',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('categoria', sa.String(100), nullable=False),
        sa.Column('codigo_cie10', sa.String(20), nullable=True),
        sa.Column('esta_publicado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('archivo_media_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['archivo_media_id'], ['archivos_media.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('ix_enfermedades_id', 'enfermedades_ocupacionales', ['id'])
    op.create_index('ix_enfermedades_slug', 'enfermedades_ocupacionales', ['slug'])
    op.create_index('ix_enfermedades_categoria', 'enfermedades_ocupacionales', ['categoria'])
    op.create_index('ix_enfermedades_eliminado', 'enfermedades_ocupacionales', ['eliminado_en'])

    # Tabla: ejercicios
    op.create_table(
        'ejercicios',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('categoria_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('duracion_segundos', sa.Integer(), nullable=False),
        sa.Column('repeticiones', sa.Integer(), nullable=True),
        sa.Column('series', sa.Integer(), nullable=False),
        sa.Column('nivel_dificultad', sa.Enum('principiante', 'intermedio', 'avanzado', name='nivel_ejercicio_enum'), nullable=False),
        sa.Column('parte_cuerpo', sa.String(100), nullable=False),
        sa.Column('posicion_inicial', sa.String(100), nullable=True),
        sa.Column('requiere_material', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('esta_publicado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('esta_destacado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('archivo_media_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['archivo_media_id'], ['archivos_media.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['categoria_id'], ['categorias_ejercicios.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('ix_ejercicios_id', 'ejercicios', ['id'])
    op.create_index('ix_ejercicios_slug', 'ejercicios', ['slug'])
    op.create_index('ix_ejercicios_categoria', 'ejercicios', ['categoria_id'])
    op.create_index('ix_ejercicios_publicado', 'ejercicios', ['esta_publicado'])
    op.create_index('ix_ejercicios_eliminado', 'ejercicios', ['eliminado_en'])
    op.create_index('ix_ejercicios_parte_cuerpo', 'ejercicios', ['parte_cuerpo'])

    # Tabla: rutinas_pausas_activas
    op.create_table(
        'rutinas_pausas_activas',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('duracion_total_minutos', sa.Integer(), nullable=False),
        sa.Column('nivel_dificultad', sa.Enum('principiante', 'intermedio', 'avanzado', name='nivel_rutina_enum'), nullable=False),
        sa.Column('esta_publicado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('es_predeterminado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('esta_destacado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('veces_completada', sa.Integer(), server_default='0', nullable=False),
        sa.Column('archivo_media_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['archivo_media_id'], ['archivos_media.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('ix_rutinas_id', 'rutinas_pausas_activas', ['id'])
    op.create_index('ix_rutinas_slug', 'rutinas_pausas_activas', ['slug'])
    op.create_index('ix_rutinas_publicado', 'rutinas_pausas_activas', ['esta_publicado'])
    op.create_index('ix_rutinas_eliminado', 'rutinas_pausas_activas', ['eliminado_en'])

    # Tabla: ejercicios_rutina
    op.create_table(
        'ejercicios_rutina',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('rutina_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ejercicio_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False),
        sa.Column('duracion_segundos_override', sa.Integer(), nullable=True),
        sa.Column('repeticiones_override', sa.Integer(), nullable=True),
        sa.Column('descanso_segundos', sa.Integer(), nullable=False),
        sa.Column('es_obligatorio', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['ejercicio_id'], ['ejercicios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['rutina_id'], ['rutinas_pausas_activas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('rutina_id', 'ejercicio_id', 'orden', name='uq_ejercicio_rutina_orden'),
    )
    op.create_index('ix_ej_rutina_id', 'ejercicios_rutina', ['id'])
    op.create_index('ix_ej_rutina_rutina', 'ejercicios_rutina', ['rutina_id'])
    op.create_index('ix_ej_rutina_ejercicio', 'ejercicios_rutina', ['ejercicio_id'])

    # Tabla: progreso_usuario
    op.create_table(
        'progreso_usuario',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dispositivo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tipo_actividad', sa.Enum('rutina', 'ejercicio', 'contenido', name='tipo_actividad_enum'), nullable=False),
        sa.Column('referencia_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tipo_referencia', sa.String(50), nullable=False),
        sa.Column('duracion_real_segundos', sa.Integer(), nullable=True),
        sa.Column('completado', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('porcentaje_completado', sa.Integer(), server_default='100', nullable=False),
        sa.Column('puntos_ganados', sa.Integer(), server_default='0', nullable=False),
        sa.Column('notas', sa.Text(), nullable=True),
        sa.Column('realizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['dispositivo_id'], ['dispositivos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_progreso_id', 'progreso_usuario', ['id'])
    op.create_index('ix_progreso_dispositivo', 'progreso_usuario', ['dispositivo_id'])
    op.create_index('ix_progreso_tipo_actividad', 'progreso_usuario', ['tipo_actividad'])
    op.create_index('ix_progreso_referencia', 'progreso_usuario', ['referencia_id'])
    op.create_index('ix_progreso_realizado', 'progreso_usuario', ['realizado_en'])

    # Tabla: recordatorios
    op.create_table(
        'recordatorios',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dispositivo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('titulo', sa.String(255), nullable=False),
        sa.Column('mensaje', sa.Text(), nullable=True),
        sa.Column('tipo', sa.Enum('pausa_activa', 'hidratacion', 'postura', 'respiracion', 'personalizado', name='tipo_recordatorio_enum'), nullable=False),
        sa.Column('hora', sa.Time(), nullable=False),
        sa.Column('dias_semana', postgresql.ARRAY(sa.Integer()), nullable=False),
        sa.Column('esta_activo', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('rutina_sugerida_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['dispositivo_id'], ['dispositivos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['rutina_sugerida_id'], ['rutinas_pausas_activas.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_recordatorios_id', 'recordatorios', ['id'])
    op.create_index('ix_recordatorios_dispositivo', 'recordatorios', ['dispositivo_id'])
    op.create_index('ix_recordatorios_tipo', 'recordatorios', ['tipo'])
    op.create_index('ix_recordatorios_eliminado', 'recordatorios', ['eliminado_en'])

    # Tabla: registros_emocionales
    op.create_table(
        'registros_emocionales',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dispositivo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('emocion_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('intensidad', sa.Integer(), nullable=False),
        sa.Column('contexto', sa.String(100), nullable=True),
        sa.Column('notas', sa.Text(), nullable=True),
        sa.Column('ubicacion_cuerpo', sa.String(100), nullable=True),
        sa.Column('registrado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['dispositivo_id'], ['dispositivos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['emocion_id'], ['emociones.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_reg_emocionales_id', 'registros_emocionales', ['id'])
    op.create_index('ix_reg_emocionales_dispositivo', 'registros_emocionales', ['dispositivo_id'])
    op.create_index('ix_reg_emocionales_emocion', 'registros_emocionales', ['emocion_id'])
    op.create_index('ix_reg_emocionales_registrado', 'registros_emocionales', ['registrado_en'])

    # Tabla: recomendaciones_emocionales
    op.create_table(
        'recomendaciones_emocionales',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('emocion_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tipo_recomendacion', sa.String(50), nullable=False),
        sa.Column('referencia_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('razon', sa.Text(), nullable=True),
        sa.Column('prioridad', sa.Integer(), nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['emocion_id'], ['emociones.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rec_emocionales_id', 'recomendaciones_emocionales', ['id'])
    op.create_index('ix_rec_emocionales_emocion', 'recomendaciones_emocionales', ['emocion_id'])
    op.create_index('ix_rec_emocionales_referencia', 'recomendaciones_emocionales', ['referencia_id'])

    # Tabla: consejos
    op.create_table(
        'consejos',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('categoria', sa.String(100), nullable=False),
        sa.Column('esta_publicado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False),
        sa.Column('archivo_media_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['archivo_media_id'], ['archivos_media.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('ix_consejos_id', 'consejos', ['id'])
    op.create_index('ix_consejos_slug', 'consejos', ['slug'])
    op.create_index('ix_consejos_categoria', 'consejos', ['categoria'])
    op.create_index('ix_consejos_publicado', 'consejos', ['esta_publicado'])
    op.create_index('ix_consejos_eliminado', 'consejos', ['eliminado_en'])

    # Tabla: mensajes_motivacionales
    op.create_table(
        'mensajes_motivacionales',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('autor', sa.String(255), nullable=True),
        sa.Column('categoria', sa.String(100), nullable=False),
        sa.Column('esta_publicado', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('eliminado_en', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_mensajes_id', 'mensajes_motivacionales', ['id'])
    op.create_index('ix_mensajes_publicado', 'mensajes_motivacionales', ['esta_publicado'])
    op.create_index('ix_mensajes_eliminado', 'mensajes_motivacionales', ['eliminado_en'])

    # Tabla: registros_auditoria
    op.create_table(
        'registros_auditoria',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('accion', sa.Enum('CREATE', 'UPDATE', 'DELETE', name='accion_auditoria_enum'), nullable=False),
        sa.Column('tabla_afectada', sa.String(100), nullable=False),
        sa.Column('registro_id', sa.String(255), nullable=False),
        sa.Column('usuario_id', sa.String(255), nullable=True),
        sa.Column('dispositivo_id', sa.String(255), nullable=True),
        sa.Column('direccion_ip', sa.String(45), nullable=True),
        sa.Column('valores_anteriores', sa.Text(), nullable=True),
        sa.Column('valores_nuevos', sa.Text(), nullable=True),
        sa.Column('razon_cambio', sa.String(500), nullable=True),
        sa.Column('endpoint_api', sa.String(255), nullable=True),
        sa.Column('id_solicitud', sa.String(100), nullable=True),
        sa.Column('ocurrido_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_auditoria_id', 'registros_auditoria', ['id'])
    op.create_index('ix_auditoria_accion', 'registros_auditoria', ['accion'])
    op.create_index('ix_auditoria_tabla', 'registros_auditoria', ['tabla_afectada'])
    op.create_index('ix_auditoria_registro', 'registros_auditoria', ['registro_id'])
    op.create_index('ix_auditoria_ocurrido', 'registros_auditoria', ['ocurrido_en'])


def downgrade() -> None:
    """Revertir la migración inicial (eliminar todas las tablas)."""
    op.drop_table('registros_auditoria')
    op.drop_table('mensajes_motivacionales')
    op.drop_table('consejos')
    op.drop_table('recomendaciones_emocionales')
    op.drop_table('registros_emocionales')
    op.drop_table('recordatorios')
    op.drop_table('progreso_usuario')
    op.drop_table('ejercicios_rutina')
    op.drop_table('rutinas_pausas_activas')
    op.drop_table('ejercicios')
    op.drop_table('enfermedades_ocupacionales')
    op.drop_table('contenidos_ergonomicos')
    op.drop_table('emociones')
    op.drop_table('categorias_ejercicios')
    op.drop_table('traducciones')
    op.drop_table('preferencias_usuario')
    op.drop_table('dispositivos')
    op.drop_table('archivos_media')
    op.drop_table('usuarios')
    op.drop_table('idiomas')

    # Eliminar enums
    op.execute('DROP TYPE IF EXISTS rol_usuario_enum')
    op.execute('DROP TYPE IF EXISTS tipo_recurso_enum')
    op.execute('DROP TYPE IF EXISTS nivel_experiencia_enum')
    op.execute('DROP TYPE IF EXISTS tema_enum')
    op.execute('DROP TYPE IF EXISTS tipo_contenido_enum')
    op.execute('DROP TYPE IF EXISTS nivel_dificultad_contenido_enum')
    op.execute('DROP TYPE IF EXISTS nivel_ejercicio_enum')
    op.execute('DROP TYPE IF EXISTS tipo_recordatorio_enum')
    op.execute('DROP TYPE IF EXISTS tipo_actividad_enum')
    op.execute('DROP TYPE IF EXISTS nivel_rutina_enum')
    op.execute('DROP TYPE IF EXISTS accion_auditoria_enum')