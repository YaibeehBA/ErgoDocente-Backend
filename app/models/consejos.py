import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.archivos_media import ArchivoMedia
from app.models.base import ModeloTranslatable


class Consejo(ModeloTranslatable):
    """
    Tabla: consejos
    Descripción: Tips cortos y prácticos de ergonomía para docentes.
    Se muestran como tarjetas en la app.
    """
    __tablename__ = "consejos"

    slug: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True,
    )
    categoria: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True,
        comment="postura, iluminacion, voz, descanso, ergonomia",
    )
    esta_publicado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false", index=True,
    )
    orden: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0,
    )
    archivo_media_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("archivos_media.id", ondelete="SET NULL"),
        nullable=True,
    )
    archivo_media: Mapped["ArchivoMedia | None"] = relationship(
        "ArchivoMedia", lazy="select", foreign_keys=[archivo_media_id],
    )

    def __repr__(self) -> str:
        return f"<Consejo slug={self.slug}>"