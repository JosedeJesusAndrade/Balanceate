import reflex as rx
from Balanceate.state import State
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight
from Balanceate.view.navbar import navbar

__all__ = ["config_page"]

def config_page() -> rx.Component:
    return rx.box(
        # Navbar con título 'Configuración'
        navbar(page_title="Configuración"),
        
        # Contenedor principal centrado
        rx.center(
            rx.vstack(
                rx.box(
                    rx.vstack(
                        # Título de la sección
                        rx.heading(
                            "Configuraciones de la cuenta",
                            size="4",
                            color=Colors.SUCCESS.value,
                            font_family=Font.DEFAULT.value,
                            font_weight=FontWeight.BOLD.value,
                            padding_top="15px",
                            margin_bottom="6",
                            align="center",
                        ),
                        
                        # Información del usuario
                        rx.cond(
                            State.usuario_actual,
                            rx.vstack(
                                rx.text(
                                    "Usuario: " + State.usuario_actual.nombre,
                                    font_size="1rem",
                                    font_weight="medium"
                                ),
                                rx.text(
                                    "Email: " + State.usuario_actual.email,
                                    font_size="0.9rem",
                                    color="gray.600"
                                ),
                                spacing="2",
                                width="100%"
                            )
                        ),
                        
                        # Descripción
                        rx.text(
                            "Gestiona las configuraciones de tu cuenta",
                            font_size="1.125rem",
                            color="gray.600",
                            margin_bottom="8",
                            text_align="center",
                        ),
                        
                        # Botón de cerrar sesión
                        rx.button(
                            "Cerrar sesión",
                            on_click=State.logout,
                            width="100%",
                            bg="red.500",
                            color="white",
                            size="3",
                            padding="4",
                            margin_top="6",
                            _hover={"bg": "red.600"},
                        ),
                        
                        width="100%",
                        spacing="4",
                        align_items="center",
                    ),
                    width="100%",
                    max_width="448px",
                    padding_y="8",
                    padding_x="10",
                    bg="white",
                    border_radius="xl",
                    box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                ),
                width="100%",
                spacing="6",
                padding_top="100px",  # Espacio para el navbar
                padding_x="4",
            ),
            width="100%",
        ),
        width="100%",
        min_height="100vh",
        bg="gray.50",
    )