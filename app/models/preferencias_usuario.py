import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.dispositivos import Dispositivo
    from app.models.idiomas import Idioma


class PreferenciasUsuario(ModeloBase):
    """
    Tabla: preferencias_usuario
    Descripción: Configuración personalizada asociada a cada dispositivo.
    Se crea automáticamente al registrar un dispositivo con valores por defecto.
    """
    __tablename__ = "preferencias_usuario"
    __table_args__ = (
        UniqueConstraint(
            "dispositivo_id",
            name="uq_preferencias_dispositivo",
        ),
        {"comment": "Preferencias de configuración por dispositivo"},
    )

    # ── Dispositivo ────────────────────────────────────────────────────────────
    dispositivo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("dispositivos.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
        comment="FK al dispositivo propietario de estas preferencias",
    )

    # ── Idioma ─────────────────────────────────────────────────────────────────
    idioma_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("idiomas.id", ondelete="SET NULL"),
        nullable=True,
        comment="Idioma preferido para el contenido (NULL = español por defecto)",
    )

    # ── Notificaciones ─────────────────────────────────────────────────────────
    notificaciones_habilitadas: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Notificaciones push habilitadas",
    )
    frecuencia_recordatorio_minutos: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=60,
        server_default="60",
        comment="Intervalo entre recordatorios automáticos (en minutos)",
    )

    # ── Horario laboral ────────────────────────────────────────────────────────
    hora_inicio_trabajo: Mapped[str | None] = mapped_column(
        Time,
        nullable=True,
        comment="Hora de inicio de jornada laboral (HH:MM)",
    )
    hora_fin_trabajo: Mapped[str | None] = mapped_column(
        Time,
        nullable=True,
        comment="Hora de fin de jornada laboral (HH:MM)",
    )

    # ── Perfil de actividad ────────────────────────────────────────────────────
    nivel_experiencia: Mapped[str] = mapped_column(
        Enum(
            "principiante",
            "intermedio",
            "avanzado",
            name="nivel_experiencia_enum",
        ),
        nullable=False,
        default="principiante",
        server_default="principiante",
        comment="Nivel de experiencia con ejercicios ergonómicos",
    )
    objetivo_principal: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Objetivo declarado: 'reducir dolor cervical', 'mejorar postura'",
    )
    condicion_fisica: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Condiciones físicas relevantes para filtrar ejercicios",
    )

    # ── UI/UX ──────────────────────────────────────────────────────────────────
    tema: Mapped[str] = mapped_column(
        Enum("claro", "oscuro", "sistema", name="tema_enum"),
        nullable=False,
        default="sistema",
        server_default="sistema",
        comment="Tema de la interfaz",
    )
    sonido_habilitado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Sonidos de la app habilitados",
    )

    # ── Relaciones ─────────────────────────────────────────────────────────────
    dispositivo: Mapped["Dispositivo"] = relationship(
        "Dispositivo",
        back_populates="preferencias",
        lazy="select",
    )
    idioma: Mapped["Idioma | None"] = relationship(
        "Idioma",
        lazy="select",
    )

    def __repr__(self) -> str:
        return (
            f"<PreferenciasUsuario dispositivo_id="
            f"{str(self.dispositivo_id)[:8]}... "
            f"nivel={self.nivel_experiencia}>"
        )