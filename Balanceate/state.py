import os
import reflex as rx
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Balanceate.db.db import movimientos_collection, balances_collection
from Balanceate.db.usuario_repository import UsuarioRepository
from Balanceate.models import Usuario, Movimiento, GrupoMovimientos, Balance
from Balanceate.services import auth_service, movimiento_service

# Nueva clase AppState con persistencia usando rx.LocalStorage
class AppState(rx.State):
    auth_token: str = rx.LocalStorage(
        "",
        name="auth_token", 
        sync=True
    )
    
    def set_auth_token(self, value: str):
        """Setter explícito para auth_token."""
        self.auth_token = value

load_dotenv()  # Cargar variables de entorno desde .env

class State(AppState):
    """Estado global de la aplicación que extiende AppState para persistencia."""
    # Estado de autenticación
    usuario_actual: Usuario = None
    email_login: str = ""
    password_login: str = ""
    email_registro: str = ""
    password_registro: str = ""
    nombre_registro: str = ""
    error_mensaje: str = ""

    def on_load(self):
        """Se ejecuta cuando se carga la página - verifica sesión persistente."""
        print("🔄 on_load ejecutándose...")  # Debug
        print(f"🔑 Token en localStorage: {self.auth_token[:20] if self.auth_token else 'VACÍO'}...")  # Debug
        
        if self.auth_token:
            print("✅ Token encontrado, verificando validez...")  # Debug
            usuario_id = auth_service.verificar_token(self.auth_token)
            if usuario_id:
                print(f"✅ Token válido para usuario: {usuario_id}")  # Debug
                self.cargar_usuario_por_id(usuario_id)
                print("✅ Sesión restaurada exitosamente")  # Debug
            else:
                print("❌ Token inválido, limpiando localStorage...")  # Debug
                # Token iauth_serviceido, limpiar localStorage
                self.auth_token = ""
        else:
            print("ℹ️ No hay token en localStorage")  # Debug
    
    # Estado de la aplicación
    balance: Balance = Balance(usuario_id="", total=0.0, ultima_actualizacion=datetime.now().isoformat())
    movimientos: list[Movimiento] = []
    movimientos_agrupados: list[GrupoMovimientos] = []  # Lista de grupos pre-procesada
    nombre: str = ""
    valor: float = 0.0
    
    # Control de formularios dinámicos
    tipo_seleccionado: str = ""  # "ingreso", "gasto", "deuda" o "" para ninguno
    
    # Campos adicionales para deudas
    monto_total: float = 0.0
    mensualidad: float = 0.0
    plazo: int = 0

    def seleccionar_tipo(self, tipo: str):
        """Selecciona el tipo de movimiento y muestra el formulario correspondiente."""
        if self.tipo_seleccionado == tipo:
            # Si ya está seleccionado, lo deselecciona (toggle)
            self.tipo_seleccionado = ""
        else:
            self.tipo_seleccionado = tipo
            # Limpiar campos al cambiar de tipo
            self.nombre = ""
            self.valor = 0.0
            self.monto_total = 0.0
            self.mensualidad = 0.0
            self.plazo = 0

    def set_valor(self, value: str):
        """Recibe el valor como string desde el input, intenta convertir a float."""
        try:
            self.valor = float(value)
        except (ValueError, TypeError):
            self.valor = 0.0
    
    def set_monto_total(self, value: str):
        """Recibe el monto total como string desde el input."""
        try:
            self.monto_total = float(value)
        except (ValueError, TypeError):
            self.monto_total = 0.0
    
    def set_mensualidad(self, value: str):
        """Recibe la mensualidad como string desde el input."""
        try:
            self.mensualidad = float(value)
        except (ValueError, TypeError):
            self.mensualidad = 0.0
    
    def set_plazo(self, value: str):
        """Recibe el plazo como string desde el input."""
        try:
            self.plazo = int(value)
        except (ValueError, TypeError):
            self.plazo = 0

    def actualizar_balance(self, valor: float, tipo: str):
        """Actualiza el balance según el tipo de movimiento."""
        # Asegurarse de que self.balance sea un objeto Balance
        if not isinstance(self.balance, Balance):
            self.balance = Balance(
                usuario_id=self.usuario_actual.id if self.usuario_actual else "",
                total=0.0,
                ultima_actualizacion=datetime.now().isoformat(),
                disponible=0.0,
                deudas_pendientes=0.0,
                balance_real=0.0
            )
        
        # Actualizar el total y disponible
        nuevo_total = self.balance.total
        if tipo == "ingreso":
            nuevo_total += float(valor)
        elif tipo == "gasto":
            nuevo_total -= float(valor)
        # Para deudas, no afectan el balance disponible inmediatamente
            
        # Crear un nuevo objeto Balance con el total actualizado
        self.balance = Balance(
            usuario_id=self.usuario_actual.id,
            total=float(nuevo_total),
            ultima_actualizacion=datetime.now().isoformat(),
            disponible=float(nuevo_total),
            deudas_pendientes=self.balance.deudas_pendientes,
            balance_real=float(nuevo_total) - self.balance.deudas_pendientes
        )
        
        # Actualizar en la base de datos
        balances_collection.update_one(
            {"usuario_id": self.usuario_actual.id},
            {
                "$set": {
                    "total": self.balance.total,
                    "ultima_actualizacion": self.balance.ultima_actualizacion
                }
            },
            upsert=True
        )

    def agregar_movimiento(self, tipo: str):
        """Agrega un nuevo movimiento y actualiza el balance."""
        if not self.usuario_actual:
            return
        
        # Validar datos usando el servicio
        validacion = movimiento_service.validar_datos_movimiento(
            tipo=tipo,
            nombre=self.nombre,
            valor=self.valor,
            monto_total=self.monto_total,
            mensualidad=self.mensualidad,
            plazo=self.plazo
        )
        
        if not validacion.es_valido:
            self.error_mensaje = validacion.mensaje_error
            return
            
        try:
            # Crear nuevo movimiento
            nuevo_movimiento = {
                "tipo": tipo,
                "nombre": self.nombre,
                "fecha": datetime.now().isoformat(),
                "usuario_id": self.usuario_actual.id
            }
            
            # Agregar campos según el tipo
            if tipo in ["ingreso", "gasto"]:
                valor = float(self.valor)
                nuevo_movimiento["valor"] = valor
                nuevo_movimiento["monto_total"] = 0.0
                nuevo_movimiento["mensualidad"] = 0.0
                nuevo_movimiento["plazo"] = 0
            elif tipo == "deuda":
                nuevo_movimiento["valor"] = float(self.mensualidad)  # Para compatibilidad en visualización
                nuevo_movimiento["monto_total"] = float(self.monto_total)
                nuevo_movimiento["mensualidad"] = float(self.mensualidad)
                nuevo_movimiento["plazo"] = int(self.plazo)
            
            # Guardar en la base de datos
            movimientos_collection.insert_one(nuevo_movimiento)
            
            # Actualizar el balance (solo para ingreso/gasto)
            if tipo in ["ingreso", "gasto"]:
                self.actualizar_balance(float(self.valor), tipo)
            
            # Limpiar campos
            self.nombre = ""
            self.valor = 0.0
            self.monto_total = 0.0
            self.mensualidad = 0.0
            self.plazo = 0
            self.tipo_seleccionado = ""  # Ocultar formulario
            
            # Recargar movimientos
            self.cargar_movimientos()
            
        except (ValueError, TypeError) as e:
            self.error_mensaje = f"Error al agregar movimiento: {str(e)}"

    def cargar_movimientos(self):
        """Carga datos desde MongoDB y actualiza balance."""
        query = {}
        if self.usuario_actual:
            query["usuario_id"] = self.usuario_actual.id
            
        # Limitar los resultados para mejorar performance
        docs = list(movimientos_collection.find(query).sort("fecha", -1).limit(100))
        
        # Convertir documentos a objetos Movimiento usando el servicio
        self.movimientos = movimiento_service.convertir_documentos_a_movimientos(docs)
        
        # Agrupar movimientos por fecha usando el servicio
        self.movimientos_agrupados = movimiento_service.agrupar_movimientos_por_fecha(self.movimientos)
        
        # Calcular balance usando el servicio
        self.balance = movimiento_service.calcular_balance_desde_documentos(
            docs, 
            self.usuario_actual.id if self.usuario_actual else ""
        )



    def iniciar(self):
        self.cargar_movimientos()

    def set_nombre_registro(self, nombre: str):
        """Actualiza el nombre para el registro."""
        self.nombre_registro = nombre

    def set_email_registro(self, email: str):
        """Actualiza el email para el registro."""
        self.email_registro = email

    def set_password_registro(self, password: str):
        """Actualiza la contraseña para el registro."""
        self.password_registro = password

    @rx.event(background=True)
    async def registrar_usuario(self):
        """Registra un nuevo usuario."""
        print("Iniciando proceso de registro...")  # Debug
        
        async with self:
            try:
                # Validación de campos
                if not self.email_registro or not self.password_registro or not self.nombre_registro:
                    self.error_mensaje = "Todos los campos son requeridos"
                    return

                # Validación básica de email
                if "@" not in self.email_registro or "." not in self.email_registro:
                    self.error_mensaje = "Por favor ingresa un email válido"
                    return

                # Validación de longitud de contraseña
                if len(self.password_registro) < 6:
                    self.error_mensaje = "La contraseña debe tener al menos 6 caracteres"
                    return
                    
                print(f"Registrando nuevo usuario: {self.email_registro}")  # Debug
                    
                try:
                    # Hash de la contraseña usando el servicio
                    hashed_password = auth_service.hash_password(self.password_registro)
                    
                    # Crear usuario usando el repository
                    usuario_id = UsuarioRepository.crear(
                        email=self.email_registro,
                        password_hash=hashed_password,
                        nombre=self.nombre_registro
                    )
                    print(f"Usuario creado con ID: {usuario_id}")  # Debug
                    
                    # Crear usuario en el estado
                    self.usuario_actual = Usuario(
                        id=usuario_id,
                        email=self.email_registro.lower().strip(),
                        nombre=self.nombre_registro.strip()
                    )
                    
                    # Guardar sesión
                    if not self.guardar_sesion(usuario_id):
                        raise Exception("No se pudo guardar la sesión")
                    
                    print("Sesión guardada")  # Debug
                    
                    # Inicializar balance para el nuevo usuario
                    try:
                        # Guardar balance inicial en la base de datos primero
                        balance_inicial = {
                            "usuario_id": usuario_id,
                            "total": 0.0,
                            "ultima_actualizacion": datetime.now().isoformat()
                        }
                        
                        resultado_balance = balances_collection.insert_one(balance_inicial)
                        if not resultado_balance.inserted_id:
                            raise Exception("No se pudo crear el balance inicial")
                        
                        # Actualizar el balance en el estado
                        self.balance = Balance(
                            usuario_id=usuario_id,
                            total=0.0,
                            ultima_actualizacion=datetime.now().isoformat()
                        )
                    except Exception as e:
                        print(f"Error al crear balance: {str(e)}")
                        raise Exception("Error al crear el balance inicial")
                    
                    # Limpiar campos
                    self.email_registro = ""
                    self.password_registro = ""
                    self.nombre_registro = ""
                    self.error_mensaje = ""
                    
                    print("Registro exitoso, redirigiendo...")  # Debug
                    
                    # Forzar la actualización del estado y la redirección
                    return rx.redirect("/")
                    
                except Exception as e:
                    # Si algo falla durante el proceso, intentar limpiar datos parcialmente creados
                    if usuario_id:
                        try:
                            UsuarioRepository.eliminar(usuario_id)
                            balances_collection.delete_one({"usuario_id": usuario_id})
                        except:
                            pass
                    raise e
                    
            except Exception as e:
                print(f"Error en registro: {str(e)}")  # Debug
                self.error_mensaje = "Ocurrió un error al registrar el usuario. Por favor intenta nuevamente."

    @rx.event(background=True)
    async def login(self):
        """Inicia sesión de usuario."""
        print("Iniciando proceso de login...")  # Debug
        
        async with self:
            if not self.email_login or not self.password_login:
                self.error_mensaje = "Email y contraseña son requeridos"
                return

            try:
                # Buscar usuario por email usando repository
                print(f"Buscando usuario con email: {self.email_login}")  # Debug
                usuario = UsuarioRepository.buscar_por_email(self.email_login)
                
                # Verificar si existe el usuario
                if not usuario:
                    print("Usuario no encontrado")  # Debug
                    self.error_mensaje = "Email o contraseña incorrectos"
                    return
                    
                # Verificar la contraseña usando el servicio
                if not auth_service.verificar_password(
                    self.password_login,
                    usuario["password"]
                ):
                    self.error_mensaje = "Email o contraseña incorrectos"
                    return
                    
                # Actualizar estado con usuario encontrado
                self.usuario_actual = Usuario(
                    id=str(usuario["_id"]),
                    email=usuario["email"],
                    nombre=usuario["nombre"]
                )
                
                # Guardar el token en localStorage
                self.guardar_sesion(str(usuario["_id"]))
                
                # Cargar balance del usuario
                balance = balances_collection.find_one({"usuario_id": str(usuario["_id"])})
                if balance:
                    self.balance = Balance(
                        usuario_id=str(usuario["_id"]),
                        total=float(balance["total"]),  # Aseguramos que sea float
                        ultima_actualizacion=balance["ultima_actualizacion"]
                    )
                else:
                    # Si no existe balance, crear uno nuevo
                    self.balance = Balance(
                        usuario_id=str(usuario["_id"]),
                        total=0.0,
                        ultima_actualizacion=datetime.now().isoformat()
                    )
                
                # Limpiar campos
                self.email_login = ""
                self.password_login = ""
                self.error_mensaje = ""
                
                # Cargar movimientos del usuario
                self.cargar_movimientos()
                print("Login exitoso, redirigiendo...")  # Debug
                
                # Forzar la actualización del estado y la redirección
                return rx.redirect("/")
                
            except Exception as e:
                print(f"Error en login: {str(e)}")  # Para debugging
                self.error_mensaje = "Ocurrió un error al iniciar sesión"

    def get_token_from_storage(self) -> str:
        """Obtiene el token desde localStorage del navegador."""
        return self.get_token()

    def cargar_usuario_por_id(self, usuario_id: str):
        """Carga un usuario y sus datos por ID."""
        try:
            # Buscar usuario por ID usando repository
            usuario = UsuarioRepository.buscar_por_id(usuario_id)
            print(f"🔍 Buscando usuario con ID: {usuario_id}")  # Debug
            
            if usuario:
                print(f"👤 Usuario encontrado: {usuario['email']}")  # Debug
                self.usuario_actual = Usuario(
                    id=str(usuario["_id"]),
                    email=usuario["email"],
                    nombre=usuario["nombre"]
                )
                
                # Cargar balance del usuario (igual que en login)
                balance = balances_collection.find_one({"usuario_id": str(usuario["_id"])})
                if balance:
                    self.balance = Balance(
                        usuario_id=str(usuario["_id"]),
                        total=float(balance["total"]),
                        ultima_actualizacion=balance["ultima_actualizacion"]
                    )
                    print(f"💰 Balance cargado: ${balance['total']}")  # Debug
                else:
                    # Si no existe balance, crear uno nuevo
                    self.balance = Balance(
                        usuario_id=str(usuario["_id"]),
                        total=0.0,
                        ultima_actualizacion=datetime.now().isoformat()
                    )
                    print("💰 Balance inicial creado")  # Debug
                
                # Cargar movimientos del usuario
                self.cargar_movimientos()
                print(f"📊 Movimientos cargados: {len(self.movimientos)}")  # Debug
            else:
                print(f"❌ No se encontró usuario con ID: {usuario_id}")  # Debug
        except Exception as e:
            print(f"💥 Error al cargar usuario: {str(e)}")  # Debug

    def guardar_sesion(self, usuario_id: str):
        """Guarda el token en localStorage usando AppState."""
        try:
            print(f"Generando token para usuario: {usuario_id}")  # Debug
            token = auth_service.generar_token(usuario_id)
            
            if not token:
                print("Error: No se pudo generar el token")  # Debug
                return False
                
            print("Token generado correctamente")  # Debug
            # Guardar token en localStorage usando AppState
            self.set_auth_token(token)
            print("Token guardado en localStorage")  # Debug
            return True
            
        except Exception as e:
            print(f"Error al guardar sesión: {str(e)}")  # Debug
            self.error_mensaje = "Error al iniciar sesión"
            return False

    def logout(self):
        """Cerrar sesión y redirigir al login."""
        print("🚪 Iniciando logout...")  # Debug
        
        # Limpiar estado del usuario
        self.usuario_actual = None
        print("👤 Usuario actual limpiado")  # Debug
        
        # Limpiar localStorage usando AppState
        self.auth_token = ""
        print("🔑 Token eliminado de localStorage")  # Debug
        
        # Limpiar otros datos de sesión
        self.balance = Balance(usuario_id="", total=0.0, ultima_actualizacion=datetime.now().isoformat())
        self.movimientos = []
        print("📊 Datos de sesión limpiados")  # Debug
        
        print("✅ Logout completado, redirigiendo...\n")  # Debug
        return rx.redirect("/")
