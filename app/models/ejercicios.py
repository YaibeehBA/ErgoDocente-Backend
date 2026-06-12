import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloTranslatable

if TYPE_CHECKING:
    from app.models.archivos_media import ArchivoMedia
    from app.models.categorias_ejercicios import CategoriaEjercicio
    from app.models.ejercicios_rutina import EjercicioRutina
    from app.models.progreso_usuario import ProgresoUsuario


class Ejercicio(ModeloTranslatable):
    """
    Tabla: ejercicios
    Descripcion: Ejercicio individual con instrucciones, duracion y nivel.
    Puede pertenecer a multiples rutinas.
    """
    __tablename__ = "ejercicios"

    slug: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True,
        comment="URL amigable: 'rotacion-cuello-lateral'",
    )
    categoria_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categorias_ejercicios.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="Categoria del ejercicio",
    )
    duracion_segundos: Mapped[int] = mapped_column(
        Integer, nullable=False, default=30,
        comment="Duracion base del ejercicio en segundos",
    )
    repeticiones: Mapped[int | None] = mapped_column(
        Integer, nullable=True,
        comment="Numero de repeticiones (NULL si es por tiempo)",
    )
    series: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1,
        comment="Numero de series",
    )
    nivel_dificultad: Mapped[str] = mapped_column(
        Enum("principiante", "intermedio", "avanzado", name="nivel_ejercicio_enum"),
        nullable=False, default="principiante",
    )
    parte_cuerpo: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True,
        comment="Parte del cuerpo: 'cuello', 'espalda', 'manos', 'ojos'",
    )
    posicion_inicial: Mapped[str | None] = mapped_column(
        String(100), nullable=True,
        comment="Posicion de inicio: 'sentado', 'de pie', 'ambas'",
    )
    requiere_material: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false",
        comment="Indica si requiere material adicional",
    )
    esta_publicado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false", index=True,
    )
    esta_destacado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false",
    )
    archivo_media_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("archivos_media.id", ondelete="SET NULL"),
        nullable=True,
        comment="Video/GIF/imagen del ejercicio",
    )

    # -- Relaciones --
    categoria: Mapped["CategoriaEjercicio"] = relationship(
        "CategoriaEjercicio", back_populates="ejercicios", lazy="select",
    )
    archivo_media: Mapped["ArchivoMedia | None"] = relationship(
        "ArchivoMedia", lazy="select", foreign_keys=[archivo_media_id],
    )
    ejercicios_rutina: Mapped[list["EjercicioRutina"]] = relationship(
        "EjercicioRutina", back_populates="ejercicio", lazy="select",
    )
    progresos: Mapped[list["ProgresoUsuario"]] = relationship(
        "ProgresoUsuario",
        primaryjoin="and_(ProgresoUsuario.referencia_id == foreign(Ejercicio.id), "
                    "ProgresoUsuario.tipo_referencia == 'ejercicio')",
        lazy="select",
        viewonly=True,
    )

    def __repr__(self) -> str:
        return f"<Ejercicio slug={self.slug} nivel={self.nivel_dificultad}>"