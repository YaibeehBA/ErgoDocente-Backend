from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# ── Contexto de hashing de contraseñas ────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── Utilidades de contraseñas ──────────────────────────────────────────────────

def hashear_password(password: str) -> str:
    """Genera el hash bcrypt de una contraseña."""
    return pwd_context.hash(password)


def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Verifica si una contraseña plana coincide con el hash."""
    return pwd_context.verify(password_plano, password_hash)


# ── JWT (preparado para V2) ────────────────────────────────────────────────────

def crear_access_token(
    datos: dict[str, Any],
    expira_en: timedelta | None = None,
) -> str:
    """
    [V2] Genera un access token JWT firmado con HS256.
    No se usa en V1 pero está definido para no reescribir lógica.
    """
    payload = datos.copy()
    ahora = datetime.now(timezone.utc)
    expiracion = ahora + (
        expira_en or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload.update({
        "iat": ahora,
        "exp": expiracion,
        "type": "access",
    })
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def crear_refresh_token(usuario_id: str) -> str:
    """
    [V2] Genera un refresh token JWT de larga duración.
    """
    expiracion = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return crear_access_token(
        datos={"sub": usuario_id, "type": "refresh"},
        expira_en=expiracion,
    )


def crear_token_reset_password(correo: str) -> str:
    """
    [V2] Token de corta duración para recuperación de contraseña.
    """
    expiracion = timedelta(minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES)
    return crear_access_token(
        datos={"sub": correo, "type": "password_reset"},
        expira_en=expiracion,
    )


def decodificar_token(token: str) -> dict[str, Any]:
    """
    [V2] Decodifica y valida un JWT.
    Lanza JWTError si el token es inválido o expiró.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError as e:
        logger.warning("Token JWT inválido", error=str(e))
        raise


# ── Roles (preparado para V2) ──────────────────────────────────────────────────

class Rol:
    """
    [V2] Constantes de roles del sistema.
    ADMIN: acceso total a contenido, usuarios y auditoría.
    USUARIO: acceso a funcionalidades de la app (ejercicios, emociones, progreso).
    """
    ADMIN = "admin"
    USUARIO = "usuario"

    TODOS = [ADMIN, USUARIO]


# ── Device ID Utilities ────────────────────────────────────────────────────────

def sanitizar_device_id(device_id: str) -> str:
    """
    Sanitiza el device_id para evitar inyecciones.
    Solo permite caracteres alfanuméricos, guiones y puntos.
    """
    import re
    limpio = re.sub(r"[^a-zA-Z0-9\-_.]", "", device_id)
    if len(limpio) < 8:
        raise ValueError("device_id demasiado corto (mínimo 8 caracteres)")
    if len(limpio) > 255:
        raise ValueError("device_id demasiado largo (máximo 255 caracteres)")
    return limpio