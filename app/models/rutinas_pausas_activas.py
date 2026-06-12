import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.archivos_media import ArchivoMedia
from app.models.base import ModeloTranslatable
from app.models.ejercicios_rutina import EjercicioRutina


class RutinaPausaActiva(ModeloTranslatable):
    """
    Tabla: rutinas_pausas_activas
    Descripción: Secuencia guiada de ejercicios para pausas activas.
    Duración total = suma de ejercicios + descansos.
    """
    __tablename__ = "rutinas_pausas_activas"

    slug: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True,
        comment="URL amigable: 'pausa-activa-espalda-5min'",
    )
    duracion_total_minutos: Mapped[int] = mapped_column(
        Integer, nullable=False, default=5,
        comment="Duración total estimada de la rutina",
    )
    nivel_dificultad: Mapped[str] = mapped_column(
        Enum("principiante", "intermedio", "avanzado", name="nivel_rutina_enum"),
        nullable=False, default="principiante",
    )
    esta_publicado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false", index=True,
    )
    es_predeterminado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false",
        comment="Rutina sugerida para nuevos usuarios",
    )
    esta_destacado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false",
    )
    veces_completada: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0",
        comment="Contador global de completados",
    )

    # ── Media ──────────────────────────────────────────────────────────────────
    archivo_media_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("archivos_media.id", ondelete="SET NULL"),
        nullable=True,
        comment="Imagen/video de previsualización",
    )

    # ── Relaciones ─────────────────────────────────────────────────────────────
    archivo_media: Mapped["ArchivoMedia | None"] = relationship(
        "ArchivoMedia", lazy="select", foreign_keys=[archivo_media_id],
    )
    ejercicios_rutina: Mapped[list["EjercicioRutina"]] = relationship(
        "EjercicioRutina",
        back_populates="rutina",
        lazy="select",
        cascade="all, delete-orphan",
        order_by="EjercicioRutina.orden",
    )

    def __repr__(self) -> str:
        return f"<RutinaPausaActiva slug={self.slug} duracion={self.duracion_total_minutos}min>"