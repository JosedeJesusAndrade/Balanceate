import reflex as rx
from Balanceate.state import State
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight

__all__ = ['registro_page']

def registro_page() -> rx.Component:
    return rx.center(
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
                align="center",
            ),
            
            # Descripción
            rx.text(
                "Crea tu cuenta para comenzar",
                font_size="1.125rem",
                color="gray.600",
                margin_bottom="10",
                text_align="center",
                padding_x="4",
            ),
            
            # Formulario de registro
            rx.vstack(
                rx.vstack(
                    rx.input(
                        placeholder="Nombre",
                        value=State.nombre_registro,
                        on_change=State.set_nombre_registro,
                        border_color="gray.300",
                        padding="4",
                        font_size="1rem",
                        width="100%",
                        _focus={"border_color": Colors.SUCCESS.value},
                    ),
                    rx.input(
                        placeholder="Email",
                        type_="email",
                        value=State.email_registro,
                        on_change=State.set_email_registro,
                        border_color="gray.300",
                        padding="4",
                        font_size="1rem",
                        width="100%",
                        _focus={"border_color": Colors.SUCCESS.value},
                    ),
                    rx.input(
                        placeholder="Contraseña",
                        type_="password",
                        value=State.password_registro,
                        on_change=State.set_password_registro,
                        border_color="gray.300",
                        padding="4",
                        font_size="1rem",
                        width="100%",
                        _focus={"border_color": Colors.SUCCESS.value},
                    ),
                    rx.button(
                        "Registrarse",
                        on_click=State.registrar_usuario,
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
            
            # Botón volver
            rx.button(
                "Volver al login",
                on_click=rx.redirect("/"),
                variant="ghost",
                color=Colors.SUCCESS.value,
                font_size="sm",
                margin_top="6",
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
            max_width="448px",
            spacing="6",
            padding_y="10",
            padding_x="12",
            bg="white",
            border_radius="xl",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            align_items="center",
        ),
        width="100%",
        min_height="100vh",
        padding_y="12",
        bg="gray.50",
    )
