import os
import reflex as rx
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Balanceate.db.usuario_repository import UsuarioRepository
from Balanceate.db.movimiento_repository import MovimientoRepository
from Balanceate.db.balance_repository import BalanceRepository
from Balanceate.models import Usuario, Movimiento, GrupoMovimientos, Balance
from Balanceate.services import auth_service, movimiento_service, balance_service, validacion_service

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
                # Token inválido, limpiar localStorage
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

    def _cargar_balance_usuario(self, usuario_id: str):
        """
        Helper privado para cargar el balance de un usuario.
        Evita duplicación de código entre login y cargar_usuario_por_id.
        """
        balance_doc = BalanceRepository.obtener_balance_por_usuario(usuario_id)
        if balance_doc:
            self.balance = Balance(
                usuario_id=usuario_id,
                total=float(balance_doc["total"]),
                ultima_actualizacion=balance_doc["ultima_actualizacion"]
            )
            print(f"💰 Balance cargado: ${balance_doc['total']}")  # Debug
        else:
            self.balance = balance_service.crear_balance_inicial(usuario_id)
            print("💰 Balance inicial creado")  # Debug

    def actualizar_balance(self, valor: float, tipo: str):
        """Actualiza el balance según el tipo de movimiento usando el servicio."""
        # Asegurarse de que self.balance sea un objeto Balance
        if not isinstance(self.balance, Balance):
            self.balance = balance_service.crear_balance_inicial(
                self.usuario_actual.id if self.usuario_actual else ""
            )
        
        # Usar el servicio para actualizar incrementalmente
        self.balance = balance_service.actualizar_balance_incremental(
            self.balance, valor, tipo
        )
        
        # Actualizar en la base de datos
        BalanceRepository.actualizar_balance_por_usuario(
            self.usuario_actual.id,
            {
                "total": self.balance.total,
                "ultima_actualizacion": self.balance.ultima_actualizacion
            }
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
            # Construir el movimiento usando el servicio
            nuevo_movimiento = movimiento_service.construir_movimiento(
                tipo=tipo,
                nombre=self.nombre,
                usuario_id=self.usuario_actual.id,
                valor=self.valor,
                monto_total=self.monto_total,
                mensualidad=self.mensualidad,
                plazo=self.plazo
            )
            
            # Guardar en la base de datos
            MovimientoRepository.crear_movimiento(nuevo_movimiento)
            
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
        # Limitar los resultados para mejorar performance
        docs = MovimientoRepository.buscar_movimientos_por_usuario(
            self.usuario_actual.id if self.usuario_actual else "",
            limit=100
        )
        
        # Convertir documentos a objetos Movimiento usando el servicio
        self.movimientos = movimiento_service.convertir_documentos_a_movimientos(docs)
        
        # Agrupar movimientos por fecha usando el servicio
        self.movimientos_agrupados = movimiento_service.agrupar_movimientos_por_fecha(self.movimientos)
        
        # Calcular balance usando el servicio de balances
        self.balance = balance_service.calcular_balance_completo(
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
                # Validar campos usando el servicio
                validacion = validacion_service.validar_registro(
                    email=self.email_registro,
                    password=self.password_registro,
                    nombre=self.nombre_registro
                )
                
                if not validacion.es_valido:
                    self.error_mensaje = validacion.mensaje_error
                    return
                    
                print(f"Registrando nuevo usuario: {self.email_registro}")  # Debug
                    
                try:
                    # Hash de la contraseña usando el servicio
                    hashed_password = auth_service.hash_password(self.password_registro)
                    
                    # Normalizar datos antes de guardar
                    email_normalizado = validacion_service.normalizar_email(self.email_registro)
                    nombre_normalizado = validacion_service.normalizar_nombre(self.nombre_registro)
                    
                    # Crear usuario usando el repository
                    usuario_id = UsuarioRepository.crear(
                        email=email_normalizado,
                        password_hash=hashed_password,
                        nombre=nombre_normalizado
                    )
                    print(f"Usuario creado con ID: {usuario_id}")  # Debug
                    
                    # Crear usuario en el estado
                    self.usuario_actual = Usuario(
                        id=usuario_id,
                        email=email_normalizado,
                        nombre=nombre_normalizado
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
                        
                        BalanceRepository.crear_balance_inicial(balance_inicial)
                        
                        # Actualizar el balance en el estado
                        self.balance = balance_service.crear_balance_inicial(usuario_id)
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
                            BalanceRepository.eliminar_balance_por_usuario(usuario_id)
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
            # Validar campos usando el servicio
            validacion = validacion_service.validar_login(
                email=self.email_login,
                password=self.password_login
            )
            
            if not validacion.es_valido:
                self.error_mensaje = validacion.mensaje_error
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
                
                # Cargar balance del usuario usando helper
                self._cargar_balance_usuario(str(usuario["_id"]))
                
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
                
                # Cargar balance del usuario usando helper
                self._cargar_balance_usuario(str(usuario["_id"]))
                
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
