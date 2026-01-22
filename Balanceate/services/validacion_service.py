"""
Servicio para validaciones de datos de entrada.
Este módulo contiene funciones para validar datos de usuarios y formularios.
"""
import re


class ResultadoValidacion:
    """Resultado de una validación."""
    def __init__(self, es_valido: bool, mensaje_error: str = ""):
        self.es_valido = es_valido
        self.mensaje_error = mensaje_error


def validar_email(email: str) -> ResultadoValidacion:
    """
    Valida que un email tenga un formato correcto.
    
    Args:
        email: Email a validar
        
    Returns:
        ResultadoValidacion con es_valido=True si es válido
        
    Reglas:
        - No puede estar vacío
        - Debe contener @ y .
        - Debe tener formato básico: algo@algo.algo
        - No debe tener espacios
    """
    if not email or email.strip() == "":
        return ResultadoValidacion(False, "El email es requerido")
    
    email = email.strip()
    
    # Verificar que no tenga espacios
    if " " in email:
        return ResultadoValidacion(False, "El email no debe contener espacios")
    
    # Validación básica de formato
    if "@" not in email or "." not in email:
        return ResultadoValidacion(False, "Por favor ingresa un email válido")
    
    # Regex para validación más robusta
    patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron_email, email):
        return ResultadoValidacion(False, "El formato del email no es válido")
    
    # Verificar longitud razonable
    if len(email) > 254:  # Límite estándar de email
        return ResultadoValidacion(False, "El email es demasiado largo")
    
    return ResultadoValidacion(True)


def validar_password(password: str, min_length: int = 6) -> ResultadoValidacion:
    """
    Valida que una contraseña cumpla con requisitos mínimos de seguridad.
    
    Args:
        password: Contraseña a validar
        min_length: Longitud mínima requerida (default: 6)
        
    Returns:
        ResultadoValidacion con es_valido=True si es válida
        
    Reglas:
        - No puede estar vacía
        - Debe tener al menos min_length caracteres
        - No debe tener solo espacios
    """
    if not password:
        return ResultadoValidacion(False, "La contraseña es requerida")
    
    if password.strip() == "":
        return ResultadoValidacion(False, "La contraseña no puede estar vacía")
    
    if len(password) < min_length:
        return ResultadoValidacion(
            False, 
            f"La contraseña debe tener al menos {min_length} caracteres"
        )
    
    # Opcional: validar que tenga al menos un número o letra
    if not any(c.isalnum() for c in password):
        return ResultadoValidacion(
            False, 
            "La contraseña debe contener al menos una letra o número"
        )
    
    return ResultadoValidacion(True)


def validar_nombre(nombre: str) -> ResultadoValidacion:
    """
    Valida que un nombre sea válido.
    
    Args:
        nombre: Nombre a validar
        
    Returns:
        ResultadoValidacion con es_valido=True si es válido
        
    Reglas:
        - No puede estar vacío
        - Debe tener al menos 2 caracteres
        - No debe tener más de 100 caracteres
        - No debe contener solo espacios
    """
    if not nombre or nombre.strip() == "":
        return ResultadoValidacion(False, "El nombre es requerido")
    
    nombre = nombre.strip()
    
    if len(nombre) < 2:
        return ResultadoValidacion(False, "El nombre debe tener al menos 2 caracteres")
    
    if len(nombre) > 100:
        return ResultadoValidacion(False, "El nombre es demasiado largo (máximo 100 caracteres)")
    
    return ResultadoValidacion(True)


def validar_registro(email: str, password: str, nombre: str) -> ResultadoValidacion:
    """
    Valida todos los campos para el registro de un nuevo usuario.
    
    Args:
        email: Email del usuario
        password: Contraseña del usuario
        nombre: Nombre del usuario
        
    Returns:
        ResultadoValidacion con es_valido=True si todos los campos son válidos
        
    Nota:
        Valida en orden: nombre, email, password
        Retorna el primer error encontrado
    """
    # Validar nombre primero
    validacion_nombre = validar_nombre(nombre)
    if not validacion_nombre.es_valido:
        return validacion_nombre
    
    # Validar email
    validacion_email = validar_email(email)
    if not validacion_email.es_valido:
        return validacion_email
    
    # Validar password
    validacion_password = validar_password(password)
    if not validacion_password.es_valido:
        return validacion_password
    
    return ResultadoValidacion(True)


def validar_login(email: str, password: str) -> ResultadoValidacion:
    """
    Valida los campos para el login de un usuario.
    
    Args:
        email: Email del usuario
        password: Contraseña del usuario
        
    Returns:
        ResultadoValidacion con es_valido=True si ambos campos están presentes
        
    Nota:
        Para login, solo validamos que los campos no estén vacíos,
        no validamos formato porque eso se hace al registrar
    """
    if not email or email.strip() == "":
        return ResultadoValidacion(False, "El email es requerido")
    
    if not password or password.strip() == "":
        return ResultadoValidacion(False, "La contraseña es requerida")
    
    return ResultadoValidacion(True)


def normalizar_email(email: str) -> str:
    """
    Normaliza un email para consistencia en la base de datos.
    
    Args:
        email: Email a normalizar
        
    Returns:
        Email en lowercase y sin espacios
        
    Uso:
        Llamar antes de guardar o buscar emails en la DB
    """
    return email.strip().lower()


def normalizar_nombre(nombre: str) -> str:
    """
    Normaliza un nombre para consistencia.
    
    Args:
        nombre: Nombre a normalizar
        
    Returns:
        Nombre sin espacios extra al inicio/final
        
    Uso:
        Llamar antes de guardar nombres en la DB
    """
    return nombre.strip()