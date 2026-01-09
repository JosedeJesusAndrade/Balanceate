"""
Servicio de autenticación.
Maneja JWT, hashing de passwords y validación de usuarios.

"""
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import bcrypt
from jwt import encode, decode

load_dotenv()

# Configuración de JWT
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET debe estar definido en las variables de entorno")

JWT_EXPIRES_IN = timedelta(days=int(os.getenv("JWT_EXPIRES_DAYS", 7)))


def generar_token(usuario_id: str) -> str:

    payload = {
        "usuario_id": usuario_id,
        "exp": datetime.utcnow() + JWT_EXPIRES_IN
    }
    return encode(payload, JWT_SECRET, algorithm="HS256")


def verificar_token(token: str) -> str | None:

    if not token:
        print("🔒 Token vacío o nulo")
        return None
        
    try:
        payload = decode(token, JWT_SECRET, algorithms=["HS256"])
        if "usuario_id" in payload:
            usuario_id = payload["usuario_id"]
            print(f"🔓 Token válido para usuario: {usuario_id}")
            return usuario_id
        else:
            print("🔒 Token no contiene usuario_id")
            return None
    except Exception as e:
        print(f"🔒 Error al verificar token: {str(e)}")
        return None


def hash_password(password: str) -> str:

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verificar_password(password: str, password_hash: str | bytes) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        password: Contraseña en texto plano
        password_hash: Hash de la contraseña (puede venir como str o bytes desde MongoDB)
        
    Returns:
        True si la contraseña coincide, False en caso contrario
    """
    try:
        # Convertir password a bytes
        password_bytes = password.encode('utf-8')
        
        # Si password_hash ya es bytes, usarlo directamente
        # Si es string, convertirlo a bytes
        if isinstance(password_hash, str):
            password_hash_bytes = password_hash.encode('utf-8')
        else:
            password_hash_bytes = password_hash
        
        return bcrypt.checkpw(password_bytes, password_hash_bytes)
    except Exception as e:
        print(f"Error en verificar_password: {str(e)}")
        return False
