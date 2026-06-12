import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.dispositivos import Dispositivo


class ArchivoMedia(ModeloBase):
    """
    Tabla: archivos_media
    Descripción: Metadatos de archivos almacenados en Cloudinary.
    Actúa como registro maestro; las entidades referencian este ID.
    """
    __tablename__ = "archivos_media"

    # ── Cloudinary ─────────────────────────────────────────────────────────────
    public_id_cloudinary: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
        index=True,
        comment="Identificador único en Cloudinary (ej: ergodocente/ejercicios/abc123)",
    )
    url_publica: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="URL pública HTTP de Cloudinary",
    )
    url_segura: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="URL segura HTTPS de Cloudinary",
    )
    carpeta_cloudinary: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Carpeta organizacional en Cloudinary",
    )

    # ── Tipo de recurso ────────────────────────────────────────────────────────
    tipo_recurso: Mapped[str] = mapped_column(
        Enum("imagen", "video", "audio", "documento", name="tipo_recurso_enum"),
        nullable=False,
        index=True,
        comment="Tipo de recurso multimedia",
    )
    formato: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Formato del archivo: jpg, png, mp4, mp3, pdf",
    )

    # ── Dimensiones y duración ─────────────────────────────────────────────────
    tamano_bytes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Tamaño del archivo en bytes",
    )
    ancho_px: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Ancho en píxeles (imágenes y videos)",
    )
    alto_px: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Alto en píxeles (imágenes y videos)",
    )
    duracion_segundos: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Duración en segundos (audio y video)",
    )

    # ── Metadatos ──────────────────────────────────────────────────────────────
    nombre_original: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Nombre original del archivo al subirlo",
    )
    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Descripción del archivo para accesibilidad",
    )
    texto_alternativo: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Texto alternativo para accesibilidad (alt text)",
    )

    # ── Estado ─────────────────────────────────────────────────────────────────
    esta_activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="El archivo está disponible para su uso",
    )

    # ── Auditoría de subida ────────────────────────────────────────────────────
    dispositivo_subida_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("dispositivos.id", ondelete="SET NULL"),
        nullable=True,
        comment="Dispositivo desde el que se subió (NULL si fue subido por admin)",
    )

    # ── Relaciones ─────────────────────────────────────────────────────────────
    dispositivo_subida: Mapped["Dispositivo | None"] = relationship(
        "Dispositivo",
        back_populates="archivos_media",
        lazy="select",
    )

    def __repr__(self) -> str:
        return (
            f"<ArchivoMedia id={str(self.id)[:8]}... "
            f"tipo={self.tipo_recurso} formato={self.formato}>"
        )