import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.archivos_media import ArchivoMedia
from app.models.base import ModeloTranslatable


class EnfermedadOcupacional(ModeloTranslatable):
    """
    Tabla: enfermedades_ocupacionales
    Descripción: Enfermedades derivadas del trabajo docente con
    información preventiva y de tratamiento.
    """
    __tablename__ = "enfermedades_ocupacionales"

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Slug URL: 'sindrome-tunel-carpiano'",
    )
    categoria: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Categoría: musculoesquelética, vocal, visual, psicológica",
    )
    codigo_cie10: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Código CIE-10 de la enfermedad",
    )
    esta_publicado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        comment="Visible para usuarios",
    )
    archivo_media_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("archivos_media.id", ondelete="SET NULL"),
        nullable=True,
        comment="Imagen ilustrativa",
    )
    archivo_media: Mapped["ArchivoMedia | None"] = relationship(
        "ArchivoMedia",
        lazy="select",
        foreign_keys=[archivo_media_id],
    )

    def __repr__(self) -> str:
        return f"<EnfermedadOcupacional slug={self.slug}>"