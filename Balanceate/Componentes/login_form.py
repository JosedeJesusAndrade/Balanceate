import reflex as rx
from Balanceate.state import State
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight

def login_form() -> rx.Component:
    return rx.center(  # Contenedor principal centrado
        rx.vstack(
            # Logo o título de la aplicación
            rx.heading(
                "Balanceate",
                size="5",
                color=Colors.SUCCESS.value,
                font_family=Font.DEFAULT.value,
                font_weight=FontWeight.BOLD.value,
                padding_top="15px",
                margin_bottom="6",
                align="center",  # Asegura que el texto esté centrado
            ),
            
            # Descripción
            rx.text(
                "Gestiona tus finanzas de manera simple",
                font_size="1.125rem",
                color="gray.600",
                margin_bottom="10",  # Más espacio antes del formulario
                text_align="center",
                padding_x="4",  # Padding horizontal para el texto
            ),
            
            # Formulario de login
            rx.vstack(
                rx.vstack(  # Contenedor interno para los elementos del formulario
                    rx.input(
                        placeholder="Email",
                        value=State.email_login,
                        on_change=State.set_email_login,
                        type_="email",
                        border_color="gray.300",
                        padding="4",
                        font_size="1rem",
                        width="100%",
                        _focus={"border_color": Colors.SUCCESS.value},
                    ),
                    rx.input(
                        placeholder="Contraseña",
                        value=State.password_login,
                        on_change=State.set_password_login,
                        type_="password",
                        padding="4",
                        font_size="1rem",
                        width="100%",
                        border_color="gray.300",
                        _focus={"border_color": Colors.SUCCESS.value},
                    ),
                    rx.button(
                        "Iniciar Sesión",
                        on_click=State.login,
                        width="100%",
                        bg=Colors.SUCCESS.value,
                        color="white",
                        size="3",
                        padding="4",
                        margin_top="6",
                        _hover={"bg": "green.600"},
                    ),
                    width="100%",
                    spacing="5",
                ),
                width="90%",
                align_items="stretch",
            ),
        
        # Enlaces adicionales
        rx.hstack(
            rx.link(
                "¿Olvidaste tu contraseña?",
                href="#",
                color=Colors.SUCCESS.value,
                font_size="sm",
            ),
            rx.button(
                "Registrarse",
                on_click=rx.redirect("/registro"),
                variant="ghost",
                color=Colors.SUCCESS.value,
                font_size="sm",
            ),
            margin_top="6",
            spacing="4",
            justify="center",
        ),
        
        # Mensaje de error
        rx.cond(
            State.error_mensaje != "",
            rx.text(
                State.error_mensaje,
                color="red.500",
                margin_top="4",
                font_size="sm",
            ),
        ),
        
        width="100%",
        max_width="448px",  # Equivalente a container size="1"
        spacing="6",  # Más espacio entre secciones
        padding_y="10",  # Padding vertical
        padding_x="12",  # Padding horizontal aumentado
        bg="white",
        border_radius="xl",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        align_items="center",  # Centra los elementos horizontalmente
    ),
        width="100%",
        min_height="100vh",  # Usa toda la altura de la pantalla
        padding_y="12",  # Más padding vertical
        bg="gray.50"  # Fondo sutil para contraste
    )
