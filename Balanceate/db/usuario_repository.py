"""
Repository para operaciones de usuario en la base de datos.
Encapsula toda la lógica de acceso a datos relacionada con usuarios.

Este módulo implementa el Patrón Repository, proporcionando una interfaz
limpia y abstracta para las operaciones CRUD de usuarios, independiente
de la implementación específica de la base de datos.
"""
from datetime import datetime
from bson import ObjectId
from .db import usuarios_collection


class UsuarioRepository:
    """
    Repository para gestionar operaciones de usuarios en MongoDB.
    
    Responsabilidades:
        - Encapsular queries de MongoDB relacionadas con usuarios
        - Abstraer conversiones entre ObjectId y string
        - Proporcionar una API clara en lenguaje de dominio
        - Centralizar la lógica de acceso a datos de usuarios
    """
    
    @staticmethod
    def buscar_por_email(email: str) -> dict | None:
        """
        Busca un usuario por su email.
        
        Args:
            email: Email del usuario a buscar (se normaliza automáticamente)
            
        Returns:
            Documento del usuario si existe, None si no se encuentra
            
        Uso común:
            - Login: verificar credenciales
            - Registro: verificar si el email ya existe
        """
        if not email:
            return None
        
        # Normalizar email: lowercase y sin espacios
        email_normalizado = email.lower().strip()
        return usuarios_collection.find_one({"email": email_normalizado})
    
    @staticmethod
    def buscar_por_id(usuario_id: str) -> dict | None:
        """
        Busca un usuario por su ID.
        
        Args:
            usuario_id: ID del usuario en formato string
            
        Returns:
            Documento del usuario si existe, None si no se encuentra o ID inválido
            
        Uso común:
            - Restaurar sesión desde token JWT
            - Cargar perfil de usuario
            
        Nota:
            Maneja automáticamente la conversión de string a ObjectId de MongoDB.
            Si el ID no es válido, retorna None en lugar de lanzar excepción.
        """
        if not usuario_id:
            return None
        
        try:
            return usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        except Exception:
            # ID inválido o error en la búsqueda
            return None
    
    @staticmethod
    def existe_email(email: str) -> bool:
        """
        Verifica si un email ya está registrado.
        
        Args:
            email: Email a verificar
            
        Returns:
            True si el email ya existe, False en caso contrario
            
        Uso común:
            - Validación durante el registro
            - Prevenir duplicados
        """
        return UsuarioRepository.buscar_por_email(email) is not None
    
    @staticmethod
    def crear(email: str, password_hash: str, nombre: str) -> str:
        """
        Crea un nuevo usuario en la base de datos.
        
        Args:
            email: Email del usuario (se normaliza automáticamente)
            password_hash: Hash de la contraseña (ya procesado por auth_service)
            nombre: Nombre del usuario
            
        Returns:
            ID del usuario creado en formato string
            
        Raises:
            ValueError: Si el email ya está registrado
            Exception: Si falla la inserción en la base de datos
            
        Transformaciones automáticas:
            - Email: lowercase y sin espacios
            - Nombre: sin espacios al inicio/final
            - Fecha de registro: timestamp ISO actual
            
        Uso común:
            - Proceso de registro de nuevos usuarios
        """
        # Validar que el email no exista
        if UsuarioRepository.existe_email(email):
            raise ValueError("El email ya está registrado")
        
        # Preparar documento con datos normalizados
        nuevo_usuario = {
            "email": email.lower().strip(),
            "password": password_hash,
            "nombre": nombre.strip(),
            "fecha_registro": datetime.now().isoformat()
        }
        
        # Insertar en MongoDB
        resultado = usuarios_collection.insert_one(nuevo_usuario)
        
        if not resultado.inserted_id:
            raise Exception("No se pudo crear el usuario")
        
        return str(resultado.inserted_id)
    
    @staticmethod
    def eliminar(usuario_id: str) -> bool:
        """
        Elimina un usuario de la base de datos.
        
        Args:
            usuario_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó exitosamente, False si no se encontró o falló
            
        ADVERTENCIA:
            Esta operación es irreversible. En producción, considera implementar
            "soft delete" (marcar como eliminado) en lugar de eliminar físicamente.
            
        Uso común:
            - Feature de "eliminar cuenta"
            - Limpieza de datos en rollback de operaciones fallidas
        """
        if not usuario_id:
            return False
        
        try:
            resultado = usuarios_collection.delete_one({"_id": ObjectId(usuario_id)})
            return resultado.deleted_count > 0
        except Exception:
            return False
    
    @staticmethod
    def actualizar_nombre(usuario_id: str, nuevo_nombre: str) -> bool:
        """
        Actualiza el nombre de un usuario.
        
        Args:
            usuario_id: ID del usuario
            nuevo_nombre: Nuevo nombre (se normaliza automáticamente)
            
        Returns:
            True si se actualizó exitosamente, False en caso contrario
            
        Uso común:
            - Feature de "editar perfil"
        """
        if not usuario_id or not nuevo_nombre:
            return False
        
        try:
            resultado = usuarios_collection.update_one(
                {"_id": ObjectId(usuario_id)},
                {"$set": {"nombre": nuevo_nombre.strip()}}
            )
            return resultado.modified_count > 0
        except Exception:
            return False
    
    @staticmethod
    def actualizar_password(usuario_id: str, nuevo_password_hash: str) -> bool:
        """
        Actualiza la contraseña de un usuario.
        
        Args:
            usuario_id: ID del usuario
            nuevo_password_hash: Nuevo hash de contraseña (ya procesado por auth_service)
            
        Returns:
            True si se actualizó exitosamente, False en caso contrario
            
        IMPORTANTE:
            Este método espera recibir el hash de la contraseña, NO la contraseña en texto plano.
            El hashing debe hacerse en auth_service antes de llamar este método.
            
        Uso común:
            - Feature de "cambiar contraseña"
            - Reset de contraseña olvidada
        """
        if not usuario_id or not nuevo_password_hash:
            return False
        
        try:
            resultado = usuarios_collection.update_one(
                {"_id": ObjectId(usuario_id)},
                {"$set": {"password": nuevo_password_hash}}
            )
            return resultado.modified_count > 0
        except Exception:
            return False
