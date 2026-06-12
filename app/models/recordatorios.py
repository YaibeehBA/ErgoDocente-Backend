import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text, Time
from sqlalchemy import Integer as SA_Integer
from sqlalchemy import ARRAY as SA_ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloConEliminacion

if TYPE_CHECKING:
    from app.models.dispositivos import Dispositivo
    from app.models.rutinas_pausas_activas import RutinaPausaActiva


class Recordatorio(ModeloConEliminacion):
    """
    Tabla: recordatorios
    Descripcion: Recordatorios programados del docente, configurables
    por hora, dias de la semana y tipo.
    """
    __tablename__ = "recordatorios"

    dispositivo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("dispositivos.id", ondelete="CASCADE"),
        nullable=False, index=True,
        comment="Dispositivo al que pertenece el recordatorio",
    )
    titulo: Mapped[str] = mapped_column(
        String(255), nullable=False,
        comment="Titulo del recordatorio",
    )
    mensaje: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="Mensaje completo de la notificacion",
    )
    tipo: Mapped[str] = mapped_column(
        Enum(
            "pausa_activa", "hidratacion", "postura",
            "respiracion", "personalizado",
            name="tipo_recordatorio_enum",
        ),
        nullable=False, default="pausa_activa", index=True,
    )
    hora: Mapped[str] = mapped_column(
        Time, nullable=False,
        comment="Hora del dia para el recordatorio (HH:MM:SS)",
    )
    dias_semana: Mapped[list[int]] = mapped_column(
        SA_ARRAY(SA_Integer),
        nullable=False,
        default=list,
        comment="Dias activos: [1,2,3,4,5] = Lunes a Viernes",
    )
    esta_activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true",
        comment="Recordatorio habilitado",
    )
    rutina_sugerida_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rutinas_pausas_activas.id", ondelete="SET NULL"),
        nullable=True,
        comment="Rutina que se sugiere al dispararse el recordatorio",
    )

    # -- Relaciones --
    dispositivo: Mapped["Dispositivo"] = relationship(
        "Dispositivo", back_populates="recordatorios", lazy="select",
    )
    rutina_sugerida: Mapped["RutinaPausaActiva | None"] = relationship(
        "RutinaPausaActiva", lazy="select",
        foreign_keys=[rutina_sugerida_id],
    )

    def __repr__(self) -> str:
        return f"<Recordatorio titulo={self.titulo} tipo={self.tipo}>"