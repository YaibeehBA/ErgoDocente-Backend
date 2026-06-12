"""
Recomendaciones automaticas basadas en el estado emocional del docente.
Si esta estresado -> recomendar rutina relajante.
Si esta motivado -> sugerir desafio mas dificil.
"""
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.emociones import Emocion


class RecomendacionEmocional(ModeloBase):
    """
    Tabla: recomendaciones_emocionales
    Descripcion: Relacion entre emociones y recomendaciones.
    Mapeo: cuando se registra cierta emocion -> se sugieren
    rutinas, ejercicios o contenidos especificos.
    """
    __tablename__ = "recomendaciones_emocionales"

    emocion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("emociones.id", ondelete="CASCADE"),
        nullable=False, index=True,
        comment="Emocion que dispara esta recomendacion",
    )
    tipo_recomendacion: Mapped[str] = mapped_column(
        String(50), nullable=False,
        comment="'rutina', 'ejercicio', 'contenido', 'consejo'",
    )
    referencia_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="UUID de la rutina, ejercicio, contenido o consejo",
    )
    razon: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="Explicacion de por que se recomienda",
    )
    prioridad: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1,
        comment="Orden de recomendacion (1=mas importante)",
    )

    # -- Relaciones --
    emocion: Mapped["Emocion"] = relationship(
        "Emocion",
        back_populates="recomendaciones",
        lazy="select",
    )

    def __repr__(self) -> str:
        return (
            f"<RecomendacionEmocional tipo={self.tipo_recomendacion} "
            f"emocion_id={str(self.emocion_id)[:8]}...>"
        )