"""
Repository para operaciones de balances en la base de datos.
Encapsula toda la lógica de acceso a datos relacionada con balances.

Este módulo implementa el Patrón Repository, proporcionando una interfaz
limpia y abstracta para las operaciones CRUD de balances, independiente
de la implementación específica de la base de datos.
"""
from datetime import datetime
from bson import ObjectId
from .db import balances_collection


class BalanceRepository:
    """
    Repository para gestionar operaciones de balances en MongoDB.

    Responsabilidades:
        - Encapsular queries de MongoDB relacionadas con balances
        - Abstraer conversiones entre ObjectId y string
        - Proporcionar una API clara en lenguaje de dominio
        - Centralizar la lógica de acceso a datos de balances
    """

    @staticmethod
    def obtener_balance_por_usuario(usuario_id: str) -> dict | None:
        """
        Obtiene el balance de un usuario.

        Args:
            usuario_id: ID del usuario

        Returns:
            Documento del balance si existe, None si no se encuentra

        Uso común:
            - Cargar balance al iniciar sesión
            - Mostrar balance actual en la interfaz
        """
        if not usuario_id:
            return None

        return balances_collection.find_one({"usuario_id": usuario_id})

    @staticmethod
    def actualizar_balance_por_usuario(usuario_id: str, balance_data: dict) -> bool:
        """
        Actualiza el balance de un usuario.

        Args:
            usuario_id: ID del usuario
            balance_data: Diccionario con los campos a actualizar

        Returns:
            True si se actualizó/creó, False en caso de error

        Uso común:
            - Actualizar balance después de agregar movimientos
        """
        if not usuario_id or not balance_data:
            return False

        try:
            result = balances_collection.update_one(
                {"usuario_id": usuario_id},
                {"$set": balance_data},
                upsert=True
            )
            return result.acknowledged
        except:
            return False

    @staticmethod
    def crear_balance_inicial(balance_data: dict) -> str:
        """
        Crea un balance inicial para un usuario.

        Args:
            balance_data: Diccionario con los datos del balance inicial

        Returns:
            ID del balance creado como string

        Uso común:
            - Crear balance al registrar un nuevo usuario
        """
        if not balance_data:
            raise ValueError("Los datos del balance no pueden estar vacíos")

        # Asegurar que tenga usuario_id
        if "usuario_id" not in balance_data:
            raise ValueError("El balance debe tener un usuario_id")

        result = balances_collection.insert_one(balance_data)
        return str(result.inserted_id)

    @staticmethod
    def eliminar_balance_por_usuario(usuario_id: str) -> bool:
        """
        Elimina el balance de un usuario.

        Args:
            usuario_id: ID del usuario

        Returns:
            True si se eliminó, False si no se encontró

        Uso común:
            - Limpiar datos al eliminar una cuenta de usuario
        """
        if not usuario_id:
            return False

        result = balances_collection.delete_one({"usuario_id": usuario_id})
        return result.deleted_count > 0

    @staticmethod
    def buscar_balance_por_id(balance_id: str) -> dict | None:
        """
        Busca un balance específico por su ID.

        Args:
            balance_id: ID del balance

        Returns:
            Documento del balance si existe, None si no se encuentra
        """
        if not balance_id:
            return None

        try:
            return balances_collection.find_one({"_id": ObjectId(balance_id)})
        except:
            return None

    @staticmethod
    def obtener_todos_los_balances(limit: int = 1000) -> list[dict]:
        """
        Obtiene todos los balances (para administración).

        Args:
            limit: Número máximo de balances a retornar

        Returns:
            Lista de documentos de balances
        """
        return list(balances_collection.find().limit(limit))