import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base declarativa central.
    Todos los modelos heredan de aquí para que Alembic
    pueda detectar automáticamente los cambios.
    """
    type_annotation_map = {
        uuid.UUID: UUID(as_uuid=True),
    }


# ══════════════════════════════════════════════════════════════════════════════
# MIXINS REUTILIZABLES
# ══════════════════════════════════════════════════════════════════════════════

class PKUUIDMixin:
    """Clave primaria UUID generada automáticamente."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        comment="Identificador único universal",
    )


class TimestampMixin:
    """
    Timestamps automáticos gestionados por el servidor PostgreSQL.
    - creado_en: se fija una sola vez al INSERT
    - actualizado_en: se actualiza en cada UPDATE
    """

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Fecha y hora de creación (UTC)",
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Fecha y hora de última actualización (UTC)",
    )


class SoftDeleteMixin:
    """
    Soft delete: los registros no se borran físicamente,
    se marca la fecha de eliminación.
    """

    eliminado_en: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        index=True,
        comment="Fecha de eliminación lógica (NULL = activo)",
    )

    @property
    def esta_eliminado(self) -> bool:
        """True si el registro fue eliminado lógicamente."""
        return self.eliminado_en is not None


class AuditableMixin:
    """
    Datos de auditoría: quién creó y quién actualizó por última vez.
    En V1 se almacena el device_id como string.
    En V2 se puede enriquecer con usuario_id (FK -> usuarios).
    """

    creado_por: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="device_id o user_id que creó el registro",
    )
    actualizado_por: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="device_id o user_id que actualizó el registro",
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODELOS BASE COMPUESTOS
# ══════════════════════════════════════════════════════════════════════════════

class ModeloBase(Base, PKUUIDMixin, TimestampMixin):
    """
    Modelo base para entidades sin soft delete.
    Úsalo para catálogos y tablas de configuración.
    """
    __abstract__ = True


class ModeloConEliminacion(Base, PKUUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Modelo base para entidades que requieren soft delete.
    Úsalo para entidades de negocio: ejercicios, rutinas, contenidos, etc.
    """
    __abstract__ = True

    def eliminar(self) -> None:
        """Marca el registro como eliminado."""
        self.eliminado_en = func.now()

    def restaurar(self) -> None:
        """Restaura un registro eliminado."""
        self.eliminado_en = None


class ModeloTranslatable(ModeloConEliminacion):
    """
    Modelo base para entidades que soportan traducciones
    (español + Kichwa). Las traducciones se almacenan en
    la tabla 'traducciones' con referencia polimórfica.
    """
    __abstract__ = True

    def to_dict(self) -> dict[str, Any]:
        """Serializa el modelo a diccionario (util para auditoría)."""
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }