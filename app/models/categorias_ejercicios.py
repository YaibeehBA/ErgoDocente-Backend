from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.ejercicios import Ejercicio


class CategoriaEjercicio(ModeloBase):
    """
    Tabla: categorias_ejercicios
    Descripción: Agrupa ejercicios por región corporal o tipo de actividad.
    """
    __tablename__ = "categorias_ejercicios"

    slug: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True,
        comment="Slug: 'cuello-y-hombros'",
    )
    icono_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True,
        comment="URL del ícono en Cloudinary",
    )
    color_hex: Mapped[str] = mapped_column(
        String(7), nullable=False, default="#4A90E2",
        comment="Color representativo en HEX: '#4A90E2'",
    )
    orden: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0,
        comment="Orden de presentación",
    )
    esta_activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true",
    )

    ejercicios: Mapped[list["Ejercicio"]] = relationship(
        "Ejercicio", back_populates="categoria", lazy="select",
    )

    def __repr__(self) -> str:
        return f"<CategoriaEjercicio slug={self.slug}>"