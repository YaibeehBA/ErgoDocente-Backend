import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.archivos_media import ArchivoMedia
from app.models.base import ModeloTranslatable


class ContenidoErgonomico(ModeloTranslatable):
    """
    Tabla: contenidos_ergonomicos
    Descripción: Artículos, videos e infografías sobre ergonomía docente.
    Campos traducibles: titulo, descripcion, cuerpo, resumen
    """
    __tablename__ = "contenidos_ergonomicos"

    # ── Metadatos de contenido ─────────────────────────────────────────────────
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="URL amigable: 'ergonomia-para-docentes-2024'",
    )
    tipo: Mapped[str] = mapped_column(
        Enum("articulo", "video", "infografia", "audio", name="tipo_contenido_enum"),
        nullable=False,
        index=True,
        comment="Formato del contenido",
    )
    nivel_dificultad: Mapped[str] = mapped_column(
        Enum("basico", "intermedio", "avanzado", name="nivel_dificultad_contenido_enum"),
        nullable=False,
        default="basico",
        comment="Nivel de complejidad del contenido",
    )
    tiempo_lectura_minutos: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5,
        comment="Tiempo estimado de lectura en minutos",
    )
    orden: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Orden de presentación en la app",
    )
    esta_publicado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        index=True,
        comment="Visible para usuarios",
    )
    esta_destacado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        comment="Aparece en sección de destacados",
    )
    vistas: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        comment="Contador de visualizaciones",
    )

    # ── Medios ─────────────────────────────────────────────────────────────────
    archivo_media_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("archivos_media.id", ondelete="SET NULL"),
        nullable=True,
        comment="Imagen/video/audio principal del contenido",
    )

    # ── Relaciones ─────────────────────────────────────────────────────────────
    archivo_media: Mapped["ArchivoMedia | None"] = relationship(
        "ArchivoMedia",
        lazy="select",
        foreign_keys=[archivo_media_id],
    )

    def __repr__(self) -> str:
        return f"<ContenidoErgonomico slug={self.slug} tipo={self.tipo}>"