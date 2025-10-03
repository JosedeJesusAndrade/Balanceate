import reflex as rx
from Balanceate.state import State
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight

def auth() -> rx.Component:
    return rx.cond(
        State.usuario_actual,
        
        # Si hay usuario, mostrar información y botón de logout
        rx.hstack(
            rx.text(f"Bienvenido, {State.usuario_actual.nombre}"),
            rx.button(
                "Cerrar Sesión",
                on_click=State.logout,
                color_scheme="red",
                variant="ghost",
            ),
            spacing="4",
        ),
        
        # Si no hay usuario, mostrar formularios de login y registro
        rx.vstack(
            rx.heading("Iniciar Sesión", size="2", margin_bottom="4"),
            
            # Formulario de login
            rx.vstack(
                rx.input(
                    placeholder="Email",
                    value=State.email_login,
                    on_change=State.set_email_login,
                    type_="email",
                ),
                rx.input(
                    placeholder="Contraseña",
                    value=State.password_login,
                    on_change=State.set_password_login,
                    type_="password",
                ),
                rx.button(
                    "Iniciar Sesión",
                    on_click=State.login,
                    width="100%",
                    bg=Colors.PRIMARY.value,
                ),
                spacing="3",
                padding="4",
            ),
            
            rx.divider(),
            
            rx.heading("Registro", size="2", margin_bottom="4", margin_top="4"),
            
            # Formulario de registro
            rx.vstack(
                rx.input(
                    placeholder="Nombre",
                    value=State.nombre_registro,
                    on_change=State.set_nombre_registro,
                ),
                rx.input(
                    placeholder="Email",
                    value=State.email_registro,
                    on_change=State.set_email_registro,
                    type_="email",
                ),
                rx.input(
                    placeholder="Contraseña",
                    value=State.password_registro,
                    on_change=State.set_password_registro,
                    type_="password",
                ),
                rx.button(
                    "Registrarse",
                    on_click=State.registrar_usuario,
                    width="100%",
                    bg=Colors.SUCCESS.value,
                    color="white",
                ),
                spacing="3",
                padding="4",
            ),
            
            # Mensaje de error si existe
            rx.cond(
                State.error_mensaje != "",
                rx.text(
                    State.error_mensaje,
                    color="red",
                    margin_top="4",
                ),
            ),
            
            width=["100%", "400px", "500px"],
            margin="auto",
            spacing="4",
            padding="6",
            bg=Colors.PRIMARY.value,
            border_radius="lg",
            box_shadow="lg",
        ),
    )
