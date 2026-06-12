import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModeloConEliminacion

if TYPE_CHECKING:
    from app.models.archivos_media import ArchivoMedia
    from app.models.preferencias_usuario import PreferenciasUsuario
    from app.models.progreso_usuario import ProgresoUsuario
    from app.models.recordatorios import Recordatorio
    from app.models.registros_emocionales import RegistroEmocional
    from app.models.usuarios import Usuario


class Dispositivo(ModeloConEliminacion):
    """
    Tabla: dispositivos
    Descripción: Representa una instalación única de la app ErgoDocente.
    El identificador_dispositivo es generado por la app móvil (UUID v4).
    """
    __tablename__ = "dispositivos"

    # ── Identificación ─────────────────────────────────────────────────────────
    identificador_dispositivo: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="UUID generado por la app móvil (device_id)",
    )
    nombre_dispositivo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Nombre legible: 'Samsung Galaxy S22 de Juan'",
    )

    # ── Información técnica ────────────────────────────────────────────────────
    plataforma: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="android | ios | web",
    )
    modelo_dispositivo: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Modelo del hardware: 'Samsung SM-G991B'",
    )
    version_so: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Versión del sistema operativo: 'Android 14'",
    )
    version_app: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Versión de la app instalada: '1.2.3'",
    )

    # ── Notificaciones Push (para recordatorios) ───────────────────────────────
    token_notificacion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="FCM/APNs token para notificaciones push",
    )

    # ── Estado ─────────────────────────────────────────────────────────────────
    esta_activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Dispositivo activo en el sistema",
    )
    ultimo_acceso: Mapped[str | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Último request recibido desde este dispositivo",
    )

    # ── Vínculo con usuario (V2) ───────────────────────────────────────────────
    usuario_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Usuario propietario (NULL en V1 sin autenticación)",
    )

    # ── Relaciones ─────────────────────────────────────────────────────────────
    usuario: Mapped["Usuario | None"] = relationship(
        "Usuario",
        back_populates="dispositivos",
        lazy="select",
    )
    preferencias: Mapped["PreferenciasUsuario | None"] = relationship(
        "PreferenciasUsuario",
        back_populates="dispositivo",
        uselist=False,
        lazy="select",
        cascade="all, delete-orphan",
    )
    registros_emocionales: Mapped[list["RegistroEmocional"]] = relationship(
        "RegistroEmocional",
        back_populates="dispositivo",
        lazy="select",
        cascade="all, delete-orphan",
    )
    progresos: Mapped[list["ProgresoUsuario"]] = relationship(
        "ProgresoUsuario",
        back_populates="dispositivo",
        lazy="select",
        cascade="all, delete-orphan",
    )
    recordatorios: Mapped[list["Recordatorio"]] = relationship(
        "Recordatorio",
        back_populates="dispositivo",
        lazy="select",
        cascade="all, delete-orphan",
    )
    archivos_media: Mapped[list["ArchivoMedia"]] = relationship(
        "ArchivoMedia",
        back_populates="dispositivo_subida",
        lazy="select",
    )

    def __repr__(self) -> str:
        return (
            f"<Dispositivo id={self.id} "
            f"device_id={self.identificador_dispositivo[:8]}... "
            f"plataforma={self.plataforma}>"
        )