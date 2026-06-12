from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloConEliminacion

if TYPE_CHECKING:
    from app.models.dispositivos import Dispositivo


class Usuario(ModeloConEliminacion):
    """
    Tabla: usuarios
    Descripcion: Entidad de usuario para autenticacion (V2).
    En V1 los dispositivos son la identidad principal.
    """
    __tablename__ = "usuarios"

    # -- Datos personales --
    correo: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True,
        comment="Correo electronico unico del usuario",
    )
    nombre_completo: Mapped[str] = mapped_column(
        String(255), nullable=False,
        comment="Nombre completo del usuario",
    )
    nombre_usuario: Mapped[str | None] = mapped_column(
        String(100), unique=True, nullable=True, index=True,
        comment="Nombre de usuario (alias), opcional",
    )
    telefono: Mapped[str | None] = mapped_column(
        String(20), nullable=True,
        comment="Numero de telefono",
    )
    foto_perfil_url: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="URL de foto de perfil en Cloudinary",
    )

    # -- Autenticacion (preparado para V2) --
    password_hash: Mapped[str | None] = mapped_column(
        String(255), nullable=True,
        comment="Hash bcrypt de la contrasena",
    )
    rol: Mapped[str] = mapped_column(
        Enum("admin", "usuario", name="rol_usuario_enum"),
        nullable=False, default="usuario", server_default="usuario",
        comment="Rol del usuario en el sistema",
    )

    # -- Estado de la cuenta --
    esta_activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true",
        comment="Indica si la cuenta esta activa",
    )
    verificado_en: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
        comment="Fecha en que verifico su correo electronico",
    )
    ultimo_login_en: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
        comment="Ultimo inicio de sesion exitoso",
    )
    token_reset_password: Mapped[str | None] = mapped_column(
        String(512), nullable=True,
        comment="Token para recuperacion de contrasena",
    )
    token_reset_expira_en: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
        comment="Fecha de expiracion del token de reset",
    )

    # -- OAuth (preparado para V2) --
    proveedor_oauth: Mapped[str | None] = mapped_column(
        String(50), nullable=True,
        comment="Proveedor OAuth: google, apple, facebook",
    )
    id_oauth: Mapped[str | None] = mapped_column(
        String(255), nullable=True,
        comment="ID del usuario en el proveedor OAuth",
    )

    # -- Relaciones --
    dispositivos: Mapped[list["Dispositivo"]] = relationship(
        "Dispositivo", back_populates="usuario", lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} correo={self.correo} rol={self.rol}>"