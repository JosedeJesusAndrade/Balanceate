# Balanceate.py - Archivo principal optimizado para Reflex 0.8.13
import reflex as rx
from Balanceate.state import State
from Balanceate.view.balance import balance
from Balanceate.view.navbar import navbar
from Balanceate.view.movimientos import movimientos
from Balanceate.Componentes.agregar_movimiento import agregar_movimiento
from Balanceate.view.footer import footer
from Balanceate.view.auth import auth
from Balanceate.view.login_page import login
from Balanceate.view.registro_page import registro_page
from Balanceate.view.config_page_simple import config_page
from Balanceate.view.test_localstorage import test_localstorage_page
from Balanceate.styles import styles
from rxconfig import config



def index() -> rx.Component:
    return rx.cond(
        ~State.usuario_actual,
        login(),
        rx.box(
            # Navbar fijo en la parte superior
            navbar(),
            
            # Contenido principal
            rx.box(
                rx.vstack(
                    # Balance principal
                    rx.container(
                        balance(),
                        padding_y=["1em", "1.5em", "2em"],
                        size="4",  # máx 1136px - apropiado para el contenido principal
                        center_content=True
                    ),

                    # Agregar movimiento
                    rx.container(
                        agregar_movimiento(),
                        size="3",  # máx 880px - mejor para formularios
                        center_content=True
                    ),

                    # Lista de movimientos
                    rx.container(
                        movimientos(),
                        size="4",  # máx 1136px - apropiado para tablas/listas
                        center_content=True
                    ),
                    
                    align_items="center",
                    justify="center",
                    spacing="0",  # Sin espacio extra entre secciones
                    width="100%",
                    padding_top=["140px", "130px", "180px"]  # Más espacio para navbar fijo
                ),
                width="100%",
                min_height="100vh",
            ),
            
            # Footer en la parte inferior
            footer(),
            
            # Propiedades del contenedor principal
            width="100%",
            min_height="100vh",
        )
    )
 # Configuración mejorada para Reflex 0.8.13
# Configuración optimizada para Reflex 0.8.13
app = rx.App(
    stylesheets=styles.STYLESHEETS,
    style=styles.BASE_STYLE,
)

# Agregar las páginas a la aplicación
app.add_page(
    index,
    route="/",
    title="Inicio - Balanceate",
    description="Gestión de finanzas personales",
    on_load=State.on_load  # ← Registrar verificación de sesión persistente
)

app.add_page(
    registro_page,
    route="/registro",
    title="Registro - Balanceate",
    description="Registro de nuevo usuario"
)

app.add_page(
    config_page,
    route="/config",
    title="Configuración - Balanceate",
    description="Configuraciones de la cuenta",
    on_load=State.on_load  # ← También verificar sesión en configuración
)

app.add_page(
    test_localstorage_page,
    route="/prueba",
    title="Prueba LocalStorage - Balanceate",
    description="Página de prueba para localStorage",
    on_load=State.on_load  # ← Verificar sesión también en página de pruebas
)

# Carga datos iniciales antes de arrancar
State.iniciar()
