"""
Modelos de datos de la aplicación.
Define las estructuras de Usuario, Movimiento, Balance y grupos.
"""
from pydantic import BaseModel


class Usuario(BaseModel):
    """Modelo de usuario del sistema."""
    id: str
    nombre: str
    email: str


class Movimiento(BaseModel):
    """Modelo de movimiento (ingreso/gasto/deuda)."""
    tipo: str = ""  # "ingreso", "gasto", "deuda"
    nombre: str = ""
    fecha: str = ""  # Solo hora para mostrar (HH:MM:SS)
    fecha_completa: str = ""  # Fecha completa ISO para agrupar
    valor: float = 0.0
    usuario_id: str = ""
    # Campos adicionales para deudas
    monto_total: float = 0.0  # Monto total de la deuda
    mensualidad: float = 0.0  # Pago mensual
    plazo: int = 0  # Plazo en meses


class GrupoMovimientos(BaseModel):
    """Grupo de movimientos organizados por fecha."""
    etiqueta: str = ""  # "Hoy", "Ayer" o "DD/MM/YYYY"
    movimientos: list[Movimiento] = []


class Balance(BaseModel):
    """Modelo de balance del usuario."""
    usuario_id: str = ""
    total: float = 0.0  # Balance visible actual (disponible)
    ultima_actualizacion: str = ""
    # Campos para balance expandido (futuro)
    disponible: float = 0.0  # ingresos - gastos pagados
    deudas_pendientes: float = 0.0  # suma de montos totales de deudas activas
    balance_real: float = 0.0  # disponible - deudas_pendientes
