"""
Repository para operaciones de movimientos en la base de datos.
Encapsula toda la lógica de acceso a datos relacionada con movimientos.

Este módulo implementa el Patrón Repository, proporcionando una interfaz
limpia y abstracta para las operaciones CRUD de movimientos, independiente
de la implementación específica de la base de datos.
"""
from datetime import datetime
from bson import ObjectId
from .db import movimientos_collection


class MovimientoRepository:
    """
    Repository para gestionar operaciones de movimientos en MongoDB.

    Responsabilidades:
        - Encapsular queries de MongoDB relacionadas con movimientos
        - Abstraer conversiones entre ObjectId y string
        - Proporcionar una API clara en lenguaje de dominio
        - Centralizar la lógica de acceso a datos de movimientos
    """

    @staticmethod
    def crear_movimiento(movimiento_data: dict) -> str:
        """
        Crea un nuevo movimiento en la base de datos.

        Args:
            movimiento_data: Diccionario con los datos del movimiento

        Returns:
            ID del movimiento creado como string

        Uso común:
            - Agregar nuevos ingresos, gastos o deudas
        """
        if not movimiento_data:
            raise ValueError("Los datos del movimiento no pueden estar vacíos")

        # Asegurar que tenga usuario_id
        if "usuario_id" not in movimiento_data:
            raise ValueError("El movimiento debe tener un usuario_id")

        result = movimientos_collection.insert_one(movimiento_data)
        return str(result.inserted_id)

    @staticmethod
    def buscar_movimientos_por_usuario(usuario_id: str, limit: int = 100) -> list[dict]:
        """
        Busca todos los movimientos de un usuario, ordenados por fecha descendente.

        Args:
            usuario_id: ID del usuario
            limit: Número máximo de movimientos a retornar (default: 100)

        Returns:
            Lista de documentos de movimientos

        Uso común:
            - Cargar movimientos para mostrar en la interfaz
        """
        if not usuario_id:
            return []

        return list(
            movimientos_collection
            .find({"usuario_id": usuario_id})
            .sort("fecha", -1)
            .limit(limit)
        )

    @staticmethod
    def buscar_movimiento_por_id(movimiento_id: str) -> dict | None:
        """
        Busca un movimiento específico por su ID.

        Args:
            movimiento_id: ID del movimiento

        Returns:
            Documento del movimiento si existe, None si no se encuentra
        """
        if not movimiento_id:
            return None

        try:
            return movimientos_collection.find_one({"_id": ObjectId(movimiento_id)})
        except:
            return None

    @staticmethod
    def actualizar_movimiento(movimiento_id: str, datos_actualizacion: dict) -> bool:
        """
        Actualiza un movimiento existente.

        Args:
            movimiento_id: ID del movimiento a actualizar
            datos_actualizacion: Diccionario con los campos a actualizar

        Returns:
            True si se actualizó, False si no se encontró
        """
        if not movimiento_id or not datos_actualizacion:
            return False

        try:
            result = movimientos_collection.update_one(
                {"_id": ObjectId(movimiento_id)},
                {"$set": datos_actualizacion}
            )
            return result.modified_count > 0
        except:
            return False

    @staticmethod
    def eliminar_movimiento_por_id(movimiento_id: str) -> bool:
        """
        Elimina un movimiento por su ID.

        Args:
            movimiento_id: ID del movimiento a eliminar

        Returns:
            True si se eliminó, False si no se encontró
        """
        if not movimiento_id:
            return False

        try:
            result = movimientos_collection.delete_one({"_id": ObjectId(movimiento_id)})
            return result.deleted_count > 0
        except:
            return False

    @staticmethod
    def buscar_movimientos_por_rango_fechas(
        usuario_id: str,
        fecha_inicio: str,
        fecha_fin: str,
        limit: int = 1000
    ) -> list[dict]:
        """
        Busca movimientos de un usuario dentro de un rango de fechas.

        Args:
            usuario_id: ID del usuario
            fecha_inicio: Fecha de inicio en formato ISO (YYYY-MM-DDTHH:MM:SS)
            fecha_fin: Fecha de fin en formato ISO (YYYY-MM-DDTHH:MM:SS)
            limit: Número máximo de resultados

        Returns:
            Lista de documentos de movimientos en el rango
        """
        if not usuario_id or not fecha_inicio or not fecha_fin:
            return []

        try:
            query = {
                "usuario_id": usuario_id,
                "fecha": {
                    "$gte": fecha_inicio,
                    "$lte": fecha_fin
                }
            }
            return list(
                movimientos_collection
                .find(query)
                .sort("fecha", -1)
                .limit(limit)
            )
        except:
            return []

    @staticmethod
    def contar_movimientos_por_usuario(usuario_id: str) -> int:
        """
        Cuenta el total de movimientos de un usuario.

        Args:
            usuario_id: ID del usuario

        Returns:
            Número total de movimientos
        """
        if not usuario_id:
            return 0

        return movimientos_collection.count_documents({"usuario_id": usuario_id})