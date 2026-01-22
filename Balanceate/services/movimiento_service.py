"""
Servicio para la lógica de negocio relacionada con los movimientos.
Este módulo contiene funciones puras que procesan y transforman datos de movimientos.
"""
from datetime import datetime, timedelta
from ..models import Movimiento, GrupoMovimientos, Balance


def agrupar_movimientos_por_fecha(movimientos: list[Movimiento]) -> list[GrupoMovimientos]:
    """
    Agrupa una lista de movimientos por fecha con etiquetas amigables.
    
    Args:
        movimientos: Lista de movimientos a agrupar
        
    Returns:
        Lista de GrupoMovimientos con etiquetas "Hoy", "Ayer" o fecha formateada
        
    Lógica de negocio:
        - Movimientos de hoy se etiquetan como "Hoy"
        - Movimientos de ayer se etiquetan como "Ayer"
        - Otros movimientos se etiquetan con formato DD/MM/YYYY
        - Movimientos con fecha inválida se agrupan bajo "Fecha desconocida"
    """
    if not movimientos:
        return []
    
    hoy = datetime.now().date()
    ayer = hoy - timedelta(days=1)
    grupos_dict = {}
    
    for mov in movimientos:
        try:
            fecha_obj = datetime.fromisoformat(mov.fecha_completa).date()
            
            # Determinar etiqueta según reglas de negocio
            if fecha_obj == hoy:
                etiqueta = "Hoy"
            elif fecha_obj == ayer:
                etiqueta = "Ayer"
            else:
                etiqueta = fecha_obj.strftime("%d/%m/%Y")
            
            if etiqueta not in grupos_dict:
                grupos_dict[etiqueta] = []
            grupos_dict[etiqueta].append(mov)
        except:
            # Si hay error al parsear, agrupar como "Fecha desconocida"
            if "Fecha desconocida" not in grupos_dict:
                grupos_dict["Fecha desconocida"] = []
            grupos_dict["Fecha desconocida"].append(mov)
    
    # Convertir dict a lista de GrupoMovimientos
    grupos = []
    for etiqueta, movs in grupos_dict.items():
        grupos.append(
            GrupoMovimientos(etiqueta=etiqueta, movimientos=movs)
        )
    
    return grupos


def calcular_balance_desde_documentos(docs: list[dict], usuario_id: str) -> Balance:
    """
    Calcula el balance completo a partir de documentos de MongoDB.
    
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


def convertir_documentos_a_movimientos(docs: list[dict]) -> list[Movimiento]:
    """
    Convierte documentos de MongoDB en objetos Movimiento.
    
    Args:
        docs: Lista de documentos (dicts) de movimientos desde MongoDB
        
    Returns:
        Lista de objetos Movimiento con datos validados y formateados
        
    Transformaciones aplicadas:
        - Extrae y valida campos del documento MongoDB
        - Formatea la fecha en formato HH:MM:SS para visualización
        - Redondea valores a 2 decimales
        - Maneja campos opcionales de deuda (monto_total, mensualidad, plazo)
        - Ignora documentos con datos inválidos
    """
    movimientos = []
    
    for doc in docs:
        try:
            # Extraer campos básicos
            valor = float(doc.get("valor", 0))
            tipo = doc.get("tipo", "")
            nombre = doc.get("nombre", "")
            fecha = doc.get("fecha", datetime.now().isoformat())
            usuario_id = doc.get("usuario_id", "")
            
            # Formatear la fecha para mostrar solo hora (HH:MM:SS)
            try:
                fecha_obj = datetime.fromisoformat(fecha)
                hora_formateada = fecha_obj.strftime("%H:%M:%S")
            except:
                hora_formateada = fecha
            
            # Validar y formatear el valor
            if not isinstance(valor, (int, float)):
                valor = 0.0
            valor_formateado = round(float(valor), 2)
            
            # Cargar campos adicionales para deudas
            monto_total = float(doc.get("monto_total", 0.0))
            mensualidad = float(doc.get("mensualidad", 0.0))
            plazo = int(doc.get("plazo", 0))
            
            # Crear objeto Movimiento
            movimientos.append(
                Movimiento(
                    tipo=tipo,
                    nombre=nombre,
                    fecha=hora_formateada,  # Solo hora para mostrar
                    fecha_completa=fecha,  # Fecha completa ISO para agrupar
                    valor=str(valor_formateado),  # String para evitar problemas de formato
                    usuario_id=usuario_id,
                    monto_total=monto_total,
                    mensualidad=mensualidad,
                    plazo=plazo
                )
            )
        except (ValueError, TypeError):
            # Ignorar documentos con datos inválidos
            continue
    
    return movimientos


class ResultadoValidacion:
    """Resultado de una validación de movimiento."""
    def __init__(self, es_valido: bool, mensaje_error: str = ""):
        self.es_valido = es_valido
        self.mensaje_error = mensaje_error


def validar_datos_movimiento(
    tipo: str,
    nombre: str,
    valor: float = 0.0,
    monto_total: float = 0.0,
    mensualidad: float = 0.0,
    plazo: int = 0
) -> ResultadoValidacion:
    """
    Valida los datos de un movimiento antes de guardarlo.
    
    Args:
        tipo: Tipo de movimiento ("ingreso", "gasto", "deuda")
        nombre: Nombre/descripción del movimiento
        valor: Valor del movimiento (para ingreso/gasto)
        monto_total: Monto total de la deuda
        mensualidad: Mensualidad de la deuda
        plazo: Plazo en meses de la deuda
        
    Returns:
        ResultadoValidacion con es_valido=True si pasa todas las validaciones,
        o es_valido=False con mensaje_error descriptivo
        
    Reglas de negocio:
        - Nombre es obligatorio
        - Para ingreso/gasto: el valor debe ser mayor a 0
        - Para deuda: monto_total, mensualidad y plazo deben ser mayores a 0
        - Para deuda: la mensualidad * plazo debe ser >= monto_total (coherencia)
    """
    # Validación básica: nombre obligatorio
    if not nombre or nombre.strip() == "":
        return ResultadoValidacion(False, "El nombre es obligatorio")
    
    # Validaciones específicas por tipo
    if tipo in ["ingreso", "gasto"]:
        if valor <= 0:
            return ResultadoValidacion(
                False, 
                f"El valor del {tipo} debe ser mayor a 0"
            )
    
    elif tipo == "deuda":
        if monto_total <= 0:
            return ResultadoValidacion(
                False, 
                "El monto total de la deuda debe ser mayor a 0"
            )
        
        if mensualidad <= 0:
            return ResultadoValidacion(
                False, 
                "La mensualidad debe ser mayor a 0"
            )
        
        if plazo <= 0:
            return ResultadoValidacion(
                False, 
                "El plazo debe ser al menos 1 mes"
            )
        
        # Validación de coherencia: mensualidad * plazo >= monto_total
        total_pagos = mensualidad * plazo
        if total_pagos < monto_total:
            return ResultadoValidacion(
                False,
                f"La mensualidad es insuficiente. Con ${mensualidad} durante {plazo} meses "
                f"pagarías ${total_pagos:.2f}, pero la deuda es ${monto_total:.2f}"
            )
    
    else:
        return ResultadoValidacion(
            False, 
            f"Tipo de movimiento inválido: {tipo}"
        )
    
    # Todas las validaciones pasaron
    return ResultadoValidacion(True)


def construir_movimiento(
    tipo: str,
    nombre: str,
    usuario_id: str,
    valor: float = 0.0,
    monto_total: float = 0.0,
    mensualidad: float = 0.0,
    plazo: int = 0
) -> dict:
    """
    Construye un diccionario de movimiento listo para guardar en la base de datos.
    
    Args:
        tipo: Tipo de movimiento ("ingreso", "gasto", "deuda")
        nombre: Nombre/descripción del movimiento
        usuario_id: ID del usuario propietario
        valor: Valor del movimiento (para ingreso/gasto)
        monto_total: Monto total de la deuda
        mensualidad: Mensualidad de la deuda
        plazo: Plazo en meses de la deuda
        
    Returns:
        Diccionario con todos los campos necesarios para MongoDB
        
    Nota:
        Esta función NO valida los datos. Se asume que ya fueron validados
        con validar_datos_movimiento() antes de llamar a esta función.
        
    Lógica de negocio:
        - Para ingreso/gasto: usa 'valor' como campo principal
        - Para deuda: usa 'mensualidad' como 'valor' (para compatibilidad en visualización)
        - Todos los movimientos tienen los mismos campos para consistencia
    """
    # Campos base que todos los movimientos tienen
    movimiento = {
        "tipo": tipo,
        "nombre": nombre,
        "fecha": datetime.now().isoformat(),
        "usuario_id": usuario_id
    }
    
    # Agregar campos específicos según el tipo
    if tipo in ["ingreso", "gasto"]:
        movimiento["valor"] = float(valor)
        movimiento["monto_total"] = 0.0
        movimiento["mensualidad"] = 0.0
        movimiento["plazo"] = 0
    elif tipo == "deuda":
        # Para deudas, 'valor' guarda la mensualidad para mostrar en la UI
        movimiento["valor"] = float(mensualidad)
        movimiento["monto_total"] = float(monto_total)
        movimiento["mensualidad"] = float(mensualidad)
        movimiento["plazo"] = int(plazo)
    
    return movimiento
