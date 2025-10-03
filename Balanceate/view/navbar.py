import reflex as rx
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight

def navbar(page_title: str = "Mi Billetera") -> rx.Component:
    return rx.hstack(
        # Avatar container como botón
        rx.box(
            rx.button(
                rx.avatar(
                    name="Usuario", 
                    size="6",  # Tamaño fijo - no responsive en 0.7.8
                    radius="full"
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
        
        # Button container (título principal)
        rx.box(
            rx.link(
                rx.button(
                    page_title,
                    variant="ghost", 
                    size="3",  # Tamaño fijo
                    font_weight=FontWeight.MEDIUM.value,
                    color="black",
                    font_family=Font.DEFAULT.value,
                    font_size=["0.9rem", "1rem", "1.1rem"],  # Responsive font
                    style={
                        "boxShadow": "none",
                        "background": "none",
                        "border": "none"
                    }
                ),
                href="#"
            ),
            align="center",
            justify="center",
            align_self="center",
        ),
        
        # Settings icon como botón
        rx.box(
            rx.button(
                rx.icon(
                    tag="settings", 
                    size=24,  # Tamaño fijo
                    color="black"
                ),
                variant="ghost",
                bg="none",
                box_shadow="none",
                on_click=rx.redirect("/config"),
                width="auto",
                padding="0.5rem"
            ),
            align="center",
            justify="center",
            align_self="center",
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
        padding=["0.8rem", "1rem", "1.2rem"],  # Responsive padding
        bg=Colors.PRIMARY.value,
        box_shadow="rgba(0, 0, 0, 0.1) 0px 3px 7px"
    )