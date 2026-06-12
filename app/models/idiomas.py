from typing import TYPE_CHECKING
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloBase

if TYPE_CHECKING:
    from app.models.traducciones import Traduccion
    # from app.models.preferencias_usuario import PreferenciasUsuario  # COMENTAR


class Idioma(ModeloBase):
    """
    Tabla: idiomas
    Descripción: Catálogo de idiomas disponibles en la plataforma.
    """
    __tablename__ = "idiomas"

    # ── Identificación ─────────────────────────────────────────────────────────
    codigo: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True,
        comment="Código ISO del idioma: 'es' (Español), 'kw' (Kichwa)",
    )
    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nombre del idioma en su propio idioma: 'Español', 'Kichwa'",
    )
    nombre_en_espanol: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nombre en español: 'Español', 'Kichwa'",
    )
    direccion_texto: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="ltr",
        server_default="ltr",
        comment="Dirección del texto: ltr (izq-der) o rtl (der-izq)",
    )
    bandera_emoji: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        comment="Emoji de bandera representativa: 🇪🇨",
    )

    # ── Estado ─────────────────────────────────────────────────────────────────
    es_predeterminado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        comment="Idioma predeterminado del sistema",
    )
    esta_activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Idioma disponible para selección",
    )

    # ── Relaciones ─────────────────────────────────────────────────────────────
    traducciones: Mapped[list["Traduccion"]] = relationship(
        "Traduccion",
        back_populates="idioma",
        lazy="select",
    )
    # preferencias: Mapped[list["PreferenciasUsuario"]] = relationship(  # COMENTAR
    #     "PreferenciasUsuario",
    #     back_populates="idioma",
    #     lazy="select",
    # )

    def __repr__(self) -> str:
        return f"<Idioma codigo={self.codigo} nombre={self.nombre}>"