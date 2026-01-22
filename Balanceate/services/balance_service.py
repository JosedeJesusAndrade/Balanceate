"""
Servicio para la lógica de negocio relacionada con balances.
Este módulo contiene funciones puras que procesan y calculan balances.
"""
from datetime import datetime
from ..models import Balance


def calcular_balance_completo(docs: list[dict], usuario_id: str) -> Balance:
    """
    Calcula el balance completo a partir de documentos de movimientos.
    
    Args:
        docs: Lista de documentos (dicts) de movimientos desde MongoDB
        usuario_id: ID del usuario propietario del balance
        
    Returns:
        Objeto Balance con total, disponible, deudas_pendientes y balance_real
        
    Lógica de negocio:
        - Balance total (disponible): suma de ingresos menos gastos
        - Deudas pendientes: suma de montos totales de todas las deudas
        - Balance real: disponible menos deudas pendientes
        - Las deudas NO afectan el balance disponible directamente
    """
    balance_total = 0.0
    deudas_pendientes = 0.0
    
    for doc in docs:
        try:
            tipo = doc.get("tipo", "")
            
            # Calcular balance disponible (ingresos - gastos)
            if tipo == "ingreso":
                valor = float(doc.get("valor", 0))
                balance_total += valor
            elif tipo == "gasto":
                valor = float(doc.get("valor", 0))
                balance_total -= valor
            
            # Acumular deudas pendientes (monto total de cada deuda)
            if tipo == "deuda":
                monto_total = float(doc.get("monto_total", 0))
                deudas_pendientes += monto_total
                
        except (ValueError, TypeError):
            # Ignorar documentos con datos inválidos
            continue
    
    # Validar que el balance sea un número válido
    if not isinstance(balance_total, (int, float)):
        balance_total = 0.0
    
    # Calcular los 3 tipos de balance
    disponible = float(balance_total)
    balance_real = disponible - deudas_pendientes
    
    # Crear objeto Balance con todos los campos
    return Balance(
        usuario_id=usuario_id,
        total=float(balance_total),  # Mantener compatible con UI actual
        ultima_actualizacion=datetime.now().isoformat(),
        disponible=disponible,
        deudas_pendientes=deudas_pendientes,
        balance_real=balance_real
    )


def actualizar_balance_incremental(balance_actual: Balance, valor: float, tipo: str) -> Balance:
    """
    Actualiza un balance existente de forma incremental.
    
    Args:
        balance_actual: Balance actual del usuario
        valor: Valor del movimiento a aplicar
        tipo: Tipo de movimiento ("ingreso", "gasto", "deuda")
        
    Returns:
        Nuevo objeto Balance actualizado
        
    Lógica de negocio:
        - Para ingresos: aumenta el total/disponible
        - Para gastos: disminuye el total/disponible
        - Para deudas: aumenta las deudas pendientes (NO afecta disponible)
        - Recalcula balance_real = disponible - deudas_pendientes
    """
    if not isinstance(balance_actual, Balance):
        raise ValueError("balance_actual debe ser un objeto Balance")
    
    # Copiar valores actuales
    nuevo_total = balance_actual.total
    nuevas_deudas = balance_actual.deudas_pendientes
    
    # Aplicar el movimiento según tipo
    if tipo == "ingreso":
        nuevo_total += float(valor)
    elif tipo == "gasto":
        nuevo_total -= float(valor)
    elif tipo == "deuda":
        # Las deudas no afectan el balance disponible inmediatamente
        # Solo aumentan las deudas pendientes
        nuevas_deudas += float(valor)  # valor aquí sería monto_total
    
    # Calcular valores derivados
    disponible = float(nuevo_total)
    balance_real = disponible - nuevas_deudas
    
    # Crear nuevo objeto Balance
    return Balance(
        usuario_id=balance_actual.usuario_id,
        total=nuevo_total,
        ultima_actualizacion=datetime.now().isoformat(),
        disponible=disponible,
        deudas_pendientes=nuevas_deudas,
        balance_real=balance_real
    )


def crear_balance_inicial(usuario_id: str) -> Balance:
    """
    Crea un balance inicial vacío para un nuevo usuario.
    
    Args:
        usuario_id: ID del usuario
        
    Returns:
        Objeto Balance con valores iniciales (cero)
    """
    return Balance(
        usuario_id=usuario_id,
        total=0.0,
        ultima_actualizacion=datetime.now().isoformat(),
        disponible=0.0,
        deudas_pendientes=0.0,
        balance_real=0.0
    )


def validar_balance(balance: Balance) -> bool:
    """
    Valida que un balance tenga datos consistentes.
    
    Args:
        balance: Objeto Balance a validar
        
    Returns:
        True si el balance es válido, False en caso contrario
        
    Validaciones:
        - Todos los campos numéricos deben ser números válidos
        - disponible debe ser igual a total (por ahora)
        - balance_real debe ser disponible - deudas_pendientes
        - usuario_id no debe estar vacío
    """
    if not isinstance(balance, Balance):
        return False
    
    if not balance.usuario_id or balance.usuario_id.strip() == "":
        return False
    
    # Verificar que todos los valores sean números válidos
    try:
        float(balance.total)
        float(balance.disponible)
        float(balance.deudas_pendientes)
        float(balance.balance_real)
    except (ValueError, TypeError):
        return False
    
    # Verificar consistencia: disponible = total (por ahora)
    if abs(balance.disponible - balance.total) > 0.01:  # Tolerancia para errores de redondeo
        return False
    
    # Verificar consistencia: balance_real = disponible - deudas_pendientes
    esperado_real = balance.disponible - balance.deudas_pendientes
    if abs(balance.balance_real - esperado_real) > 0.01:
        return False
    
    return True