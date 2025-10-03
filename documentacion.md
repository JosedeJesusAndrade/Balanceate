# Documentación de Balanceate

## Descripción General
Balanceate es una aplicación web desarrollada con Reflex que permite a los usuarios gestionar sus ingresos y gastos personales. La aplicación implementa un sistema de autenticación JWT y utiliza MongoDB como base de datos.

## Configuración del Proyecto

### Estructura Principal
```
Balanceate/
├── Balanceate/
│   ├── Componentes/         # Componentes reutilizables
│   ├── db/                  # Configuración de base de datos
│   ├── styles/             # Estilos y temas
│   ├── view/               # Páginas y componentes de vista
│   ├── __init__.py
│   ├── Balanceate.py      # Archivo principal
│   └── state.py           # Estado global
├── assets/                 # Recursos estáticos
├── rxconfig.py            # Configuración de Reflex
└── requirements.txt       # Dependencias
```

### Configuración de la Aplicación
```python
app = rx.App(
    stylesheets=styles.STYLESHEETS,
    style=styles.BASE_STYLE,
)
```

### Rutas Principales
- `/`: Página principal/login
- `/registro`: Página de registro
- `/movimientos`: Lista de movimientos (autenticado)

## Estructura de Datos

### Modelos Principales

1. **Usuario**
   - `id`: Identificador único
   - `nombre`: Nombre del usuario
   - `email`: Email del usuario

2. **Movimiento**
   - `tipo`: Tipo de movimiento (ingreso/gasto)
   - `nombre`: Descripción del movimiento
   - `fecha`: Fecha del movimiento
   - `valor`: Monto del movimiento
   - `usuario_id`: ID del usuario asociado

3. **Balance**
   - `usuario_id`: ID del usuario
   - `total`: Monto total actual
   - `ultima_actualizacion`: Fecha de última actualización

## Funcionalidades Principales

### 1. Gestión de Usuarios

#### Registro de Usuario
- Validación completa de campos:
  - Campos requeridos
  - Formato de email válido
  - Contraseña mínima de 6 caracteres
- Sanitización de datos:
  - Email convertido a minúsculas
  - Eliminación de espacios extras
- Verificación de email único
- Hash seguro de contraseña con bcrypt
- Creación de balance inicial
- Manejo de transacciones parciales
- Sistema de rollback en caso de error

#### Login
- Autenticación mediante email y contraseña
- Generación de token JWT
- Carga de datos del usuario y su balance

#### Persistencia de Sesión
- Almacenamiento de token en localStorage
- Verificación automática de sesión al cargar
- Logout con limpieza de datos

### 2. Gestión de Movimientos

#### Agregar Movimiento
1. Validación de datos de entrada
2. Creación del movimiento en la base de datos
3. Actualización del balance
4. Recarga de la lista de movimientos

#### Cargar Movimientos
1. Consulta a la base de datos filtrada por usuario
2. Ordenamiento por fecha descendente
3. Cálculo del balance total
4. Formateo de valores numéricos

### 3. Gestión del Balance

#### Actualización de Balance
1. Verificación del tipo de movimiento
2. Cálculo del nuevo total
3. Actualización en la base de datos
4. Actualización del estado en la aplicación

## Manejo de Datos

### Base de Datos
- **MongoDB** para almacenamiento persistente
- Colecciones:
  - `usuarios_collection`
  - `movimientos_collection`
  - `balances_collection`

### Estado de la Aplicación
- Gestión de estado mediante `rx.State`
- Estado global a través de `app_state`
- Actualización reactiva de la interfaz
- Manejo de errores y validaciones
- Persistencia de estado mediante localStorage

### Gestión del Estado Global
```python
# Inicialización del estado global
app_state = State

# Métodos de manejo de localStorage
def set_token(self, token: str):
    return rx.set_local_storage("token", token)

def get_token(self) -> str:
    return rx.get_local_storage("token")
```

## Seguridad

### Autenticación
- Tokens JWT con expiración
- Almacenamiento seguro de contraseñas con bcrypt
- Validación de sesiones activas

### Validaciones y Seguridad
- Verificación de tipos de datos
- Sanitización de entradas
  - Limpieza de espacios
  - Normalización de emails
  - Validación de formatos
- Manejo de errores en conversiones numéricas
- Sistema de rollback para operaciones fallidas
- Protección contra inyección de datos maliciosos
- Validación de tokens JWT

## Interfaz de Usuario

### Componentes Principales
1. **Auth**: Manejo de autenticación y registro
2. **Balance**: Visualización del balance actual
3. **Movimientos**: Lista de transacciones
4. **NavBar**: Navegación y estado de sesión

### Formateo de Datos
- Valores numéricos con dos decimales
- Fechas en formato ISO
- Validaciones visuales según tipo de movimiento

## Mejores Prácticas Implementadas

1. **Seguridad**
   - Hash de contraseñas
   - Tokens de sesión
   - Validación de datos

2. **Manejo de Estado**
   - Estado centralizado
   - Actualizaciones atómicas
   - Persistencia de datos

3. **Manejo de Errores**
   - Validaciones preventivas
   - Mensajes de error claros
   - Recuperación de estados inválidos

4. **Organización del Código**
   - Separación de responsabilidades
   - Modelos bien definidos
   - Funciones específicas y reutilizables
