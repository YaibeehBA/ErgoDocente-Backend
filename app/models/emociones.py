"""
Catálogo de emociones que el docente puede registrar.
Campos traducibles: nombre, descripcion
"""
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.recomendaciones_emocionales import RecomendacionEmocional


class Emocion(ModeloBase):
    """
    Tabla: emociones
    Descripción: Catálogo de estados emocionales (positivos y negativos).
    Ejemplo: feliz 😊, estresado 😰, agotado 😴, motivado 🔥
    """
    __tablename__ = "emociones"

    slug: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True,
        comment="Slug: 'estresado', 'motivado', 'agotado'",
    )
    emoji: Mapped[str] = mapped_column(
        String(10), nullable=False,
        comment="Emoji representativo: 😰",
    )
    color_hex: Mapped[str] = mapped_column(
        String(7), nullable=False, default="#888888",
        comment="Color visual en la UI",
    )
    nivel_intensidad: Mapped[int] = mapped_column(
        Integer, nullable=False, default=3,
        comment="Intensidad 1-5 (5 = más intenso)",
    )
    es_positiva: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True,
        comment="True = emoción positiva; False = negativa o neutra",
    )
    esta_activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true",
    )

    # Relaciones
    recomendaciones: Mapped[list["RecomendacionEmocional"]] = relationship(
        "RecomendacionEmocional", lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Emocion slug={self.slug} emoji={self.emoji}>"