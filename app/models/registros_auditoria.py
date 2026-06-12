"""
Registro de auditoría completo: quién cambió qué, cuándo y por qué.
Inmutable y dirigido solo a administradores.
"""
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ModeloBase


class RegistroAuditoria(ModeloBase):
    """
    Tabla: registros_auditoria
    Descripción: Bitácora inmutable de cambios en el sistema.
    Se crea automáticamente por triggers o middleware de auditoría.
    """
    __tablename__ = "registros_auditoria"

    # ── Acción ─────────────────────────────────────────────────────────────────
    accion: Mapped[str] = mapped_column(
        Enum("CREATE", "UPDATE", "DELETE", name="accion_auditoria_enum"),
        nullable=False,
        index=True,
        comment="Tipo de operación realizada",
    )
    tabla_afectada: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Tabla modificada",
    )
    registro_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="ID del registro afectado",
    )

    # ── Usuario/Dispositivo ────────────────────────────────────────────────────
    usuario_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="UUID del usuario que realizó el cambio (V2)",
    )
    dispositivo_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="UUID del dispositivo (V1)",
    )
    direccion_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
        comment="Dirección IP de la petición",
    )

    # ── Cambios ────────────────────────────────────────────────────────────────
    valores_anteriores: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="JSON con valores antes de la modificación",
    )
    valores_nuevos: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="JSON con valores después de la modificación",
    )
    razon_cambio: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Explicación del cambio (ej: 'correción de typo en descripción')",
    )

    # ── Timestamp ──────────────────────────────────────────────────────────────
    ocurrido_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        index=True,
        comment="Cuándo ocurrió el cambio",
    )

    # ── Contexto ───────────────────────────────────────────────────────────────
    endpoint_api: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Endpoint que provocó el cambio: 'POST /api/v1/dispositivos'",
    )
    id_solicitud: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Request ID para correlacionar múltiples cambios",
    )

    def __repr__(self) -> str:
        return (
            f"<RegistroAuditoria accion={self.accion} tabla={self.tabla_afectada} "
            f"id={self.registro_id[:8]}...>"
        )