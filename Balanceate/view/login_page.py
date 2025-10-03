import reflex as rx
from Balanceate.Componentes.login_form import login_form
from Balanceate.styles.colors import Colors

def login() -> rx.Component:
    return rx.box(
        # Contenedor principal con fondo decorativo
        rx.vstack(
            # Formulario de login
            login_form(),
            
            # Contenedor para información adicional
            rx.vstack(
                rx.text(
                    "¿No tienes una cuenta?",
                    color="gray.600",
                    font_size="sm",
                ),
                rx.link(
                    "Crear cuenta",
                    href="/registro",
                    color=Colors.SUCCESS.value,
                    font_weight="bold",
                    font_size="sm",
                ),
                margin_top="6",
                spacing="2",
            ),
            
            height="100vh",
            justify="center",
            align="center",
            spacing="8",
        ),
        
        # Estilos del contenedor principal
        width="100%",
        min_height="100vh",
        bg=f"linear-gradient(45deg, {Colors.PRIMARY.value}, {Colors.SUCCESS.value})",
        position="relative",
        overflow="hidden",
    )
