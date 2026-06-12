import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.ejercicios import Ejercicio
    from app.models.rutinas_pausas_activas import RutinaPausaActiva


class EjercicioRutina(ModeloBase):
    """
    Tabla: ejercicios_rutina
    Descripción: Relación N:M entre Ejercicio y RutinaPausaActiva.
    Permite que un ejercicio aparezca con configuración diferente en cada rutina.
    """
    __tablename__ = "ejercicios_rutina"
    __table_args__ = (
        UniqueConstraint(
            "rutina_id", "ejercicio_id", "orden",
            name="uq_ejercicio_rutina_orden",
        ),
        {"comment": "Ejercicios que componen cada rutina de pausa activa"},
    )

    rutina_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rutinas_pausas_activas.id", ondelete="CASCADE"),
        nullable=False, index=True,
        comment="Rutina a la que pertenece",
    )
    ejercicio_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ejercicios.id", ondelete="CASCADE"),
        nullable=False, index=True,
        comment="Ejercicio incluido",
    )
    orden: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1,
        comment="Posición del ejercicio en la rutina (1, 2, 3...)",
    )

    # ── Configuración personalizada para esta rutina ───────────────────────────
    duracion_segundos_override: Mapped[int | None] = mapped_column(
        Integer, nullable=True,
        comment="Duración específica en esta rutina (NULL = usar del ejercicio base)",
    )
    repeticiones_override: Mapped[int | None] = mapped_column(
        Integer, nullable=True,
        comment="Repeticiones específicas (NULL = usar del ejercicio base)",
    )
    descanso_segundos: Mapped[int] = mapped_column(
        Integer, nullable=False, default=10,
        comment="Segundos de descanso después de este ejercicio",
    )
    es_obligatorio: Mapped[bool] = mapped_column(
        default=True, server_default="true",
        comment="Si False, el usuario puede saltar este ejercicio",
    )

    # ── Relaciones ─────────────────────────────────────────────────────────────
    rutina: Mapped["RutinaPausaActiva"] = relationship(
        "RutinaPausaActiva", back_populates="ejercicios_rutina", lazy="select",
    )
    ejercicio: Mapped["Ejercicio"] = relationship(
        "Ejercicio", back_populates="ejercicios_rutina", lazy="select",
    )

    def __repr__(self) -> str:
        return (
            f"<EjercicioRutina orden={self.orden} "
            f"rutina={str(self.rutina_id)[:8]}...>"
        )