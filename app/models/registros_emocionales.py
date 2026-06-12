import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.dispositivos import Dispositivo
    from app.models.emociones import Emocion


class RegistroEmocional(ModeloBase):
    """
    Tabla: registros_emocionales
    Descripcion: Historial de estados emocionales registrados por dispositivo.
    El docente selecciona como se siente y el sistema genera recomendaciones.
    """
    __tablename__ = "registros_emocionales"

    # -- Dispositivo --
    dispositivo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("dispositivos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Dispositivo que registro la emocion",
    )

    # -- Emocion --
    emocion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("emociones.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="Emocion seleccionada por el docente",
    )

    # -- Intensidad y contexto --
    intensidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
        comment="Intensidad de la emocion: 1 (leve) a 5 (muy intensa)",
    )
    notas: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Notas opcionales del docente sobre su estado",
    )
    contexto: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Contexto: 'antes_clase', 'durante_clase', 'despues_clase', 'recreo'",
    )
    ubicacion_cuerpo: Mapped[str | None] = mapped_column(
    String(100),
    nullable=True,
    comment="Parte del cuerpo afectada: 'cuello', 'espalda', 'manos'",
    )

    # -- Timestamp --
    registrado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        index=True,
        comment="Cuando se registro la emocion",
    )

    # -- Relaciones --
    dispositivo: Mapped["Dispositivo"] = relationship(
        "Dispositivo",
        back_populates="registros_emocionales",
        lazy="select",
    )
    emocion: Mapped["Emocion"] = relationship(
        "Emocion",
        lazy="select",
    )

    def __repr__(self) -> str:
        return (
            f"<RegistroEmocional dispositivo_id={str(self.dispositivo_id)[:8]}... "
            f"emocion_id={str(self.emocion_id)[:8]}... "
            f"intensidad={self.intensidad}>"
        )