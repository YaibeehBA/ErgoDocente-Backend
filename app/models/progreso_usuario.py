import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.dispositivos import Dispositivo


class ProgresoUsuario(ModeloBase):
    """
    Tabla: progreso_usuario
    Descripcion: Historial de actividades completadas por dispositivo.
    """
    __tablename__ = "progreso_usuario"

    dispositivo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("dispositivos.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    tipo_actividad: Mapped[str] = mapped_column(
        Enum("rutina", "ejercicio", "contenido", name="tipo_actividad_enum"),
        nullable=False, index=True,
        comment="Tipo de actividad realizada",
    )
    referencia_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="ID de la rutina, ejercicio o contenido",
    )
    tipo_referencia: Mapped[str] = mapped_column(
        String(50), nullable=False,
        comment="'rutina', 'ejercicio', 'contenido_ergonomico'",
    )
    duracion_real_segundos: Mapped[int | None] = mapped_column(
        Integer, nullable=True,
        comment="Duracion real que tomo al usuario",
    )
    completado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true",
        comment="True = completo todo; False = abandono a la mitad",
    )
    porcentaje_completado: Mapped[int] = mapped_column(
        Integer, nullable=False, default=100, server_default="100",
        comment="Porcentaje completado: 0-100",
    )
    puntos_ganados: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0",
        comment="Puntos acumulados por esta actividad",
    )
    notas: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="Notas personales del usuario sobre la actividad",
    )
    realizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False, default=func.now(), server_default=func.now(),
        index=True,
        comment="Cuando realizo la actividad",
    )

    # -- Relaciones --
    dispositivo: Mapped["Dispositivo"] = relationship(
        "Dispositivo", back_populates="progresos", lazy="select",
    )

    def __repr__(self) -> str:
        return (
            f"<ProgresoUsuario tipo={self.tipo_actividad} "
            f"completado={self.completado}>"
        )