import reflex as rx
from Balanceate.state import State
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight

def navbar(page_title: str = "Mi Billetera") -> rx.Component:
    return rx.hstack(
        # Avatar container como botón
        rx.box(
            rx.button(
                rx.cond(
                    State.usuario_actual,
                    rx.avatar(
                        name=State.usuario_actual.nombre,
                        size="6",
                        radius="full"
                    ),
                    rx.avatar(
                        name="Usuario",
                        size="6",
                        radius="full"
                    )
                ),
                variant="ghost",
                bg="none",
                box_shadow="none",
                border="none",
                on_click=rx.redirect("/"),
                padding="0"
            ),
            align="center",
            justify="center",
            align_self="center",
        ),
        
        # Título principal
        rx.box(
            rx.heading(
                page_title,
                size="5",
                font_weight=FontWeight.MEDIUM.value,
                color="black",
                font_family=Font.DEFAULT.value,
            ),
            align="center",
            justify="center",
            align_self="center",
        ),
        
        # Settings/configuración y logout buttons
        rx.cond(
            State.usuario_actual,
            rx.hstack(
                # Botón de configuración
                rx.button(
                    rx.icon(
                        tag="settings", 
                        size=20,
                        color="black"
                    ),
                    variant="ghost",
                    bg="none",
                    box_shadow="none",
                    on_click=rx.redirect("/config"),
                    width="auto",
                    padding="0.5rem"
                ),
                # Botón de logout
                rx.button(
                    rx.icon(
                        tag="log-out", 
                        size=20,
                        color="red.600"
                    ),
                    variant="ghost",
                    bg="none",
                    box_shadow="none",
                    on_click=State.logout,
                    width="auto",
                    padding="0.5rem"
                ),
                spacing="2",
                align="center"
            ),
            # Si no hay usuario, solo mostrar configuración
            rx.button(
                rx.icon(
                    tag="settings", 
                    size=20,
                    color="black"
                ),
                variant="ghost",
                bg="none",
                box_shadow="none",
                on_click=rx.redirect("/config"),
                width="auto",
                padding="0.5rem"
            )
        ),
        
        # Propiedades del navbar
        spacing="4",
        width="100%",
        position="fixed",
        top="0",
        left="0",
        z_index="1000",
        justify="between",
        align="center",
        padding=["0.8rem", "1rem", "1.2rem"],
        bg=Colors.PRIMARY.value,
        box_shadow="rgba(0, 0, 0, 0.1) 0px 3px 7px"
    )