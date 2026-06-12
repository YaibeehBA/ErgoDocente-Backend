from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ModeloTranslatable


class MensajeMotivacional(ModeloTranslatable):
    """
    Tabla: mensajes_motivacionales
    Descripción: Frases motivacionales que se muestran en la app.
    """
    __tablename__ = "mensajes_motivacionales"

    autor: Mapped[str | None] = mapped_column(
        String(255), nullable=True,
        comment="Nombre del autor de la frase (opcional)",
    )
    categoria: Mapped[str] = mapped_column(
        String(100), nullable=False, default="general", index=True,
        comment="bienestar, motivacion, salud, docencia",
    )
    esta_publicado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false", index=True,
    )

    def __repr__(self) -> str:
        return f"<MensajeMotivacional autor={self.autor}>"