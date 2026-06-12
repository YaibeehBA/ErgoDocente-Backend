import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.idiomas import Idioma


class Traduccion(ModeloBase):
    """
    Tabla: traducciones
    Descripción: Almacén centralizado de traducciones para todas las entidades.
    """
    __tablename__ = "traducciones"
    __table_args__ = (
        UniqueConstraint(
            "tabla",
            "registro_id",
            "campo",
            "idioma_id",
            name="uq_traduccion_tabla_registro_campo_idioma",
        ),
        {"comment": "Tabla polimórfica de traducciones multi-idioma"},
    )

    # ── Referencia polimórfica ─────────────────────────────────────────────────
    tabla: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Nombre de la tabla origen: 'ejercicios', 'consejos', etc.",
    )
    registro_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="UUID del registro en la tabla origen",
    )
    campo: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Campo a traducir: 'titulo', 'descripcion', 'instrucciones'",
    )

    # ── Idioma ─────────────────────────────────────────────────────────────────
    idioma_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("idiomas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="FK al idioma de esta traducción",
    )

    # ── Contenido ──────────────────────────────────────────────────────────────
    valor: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Texto traducido",
    )

    # ── Relaciones ─────────────────────────────────────────────────────────────
    idioma: Mapped["Idioma"] = relationship(
        "Idioma",
        back_populates="traducciones",
        lazy="select",
    )

    def __repr__(self) -> str:
        return (
            f"<Traduccion tabla={self.tabla} campo={self.campo} "
            f"idioma_id={str(self.idioma_id)[:8]}...>"
        )