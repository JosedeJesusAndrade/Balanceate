import reflex as rx
from Balanceate.styles.colors import Colors
from Balanceate.styles import styles
from Balanceate.styles.fonts import Font, FontWeight

def footer() -> rx.Component:
    return rx.box(
        #footer content
        rx.vstack(
            rx.hstack(
                rx.button(
                    "Dia", size="3", 
                    color=Colors.PRIMARY.value, 
                    min_width=["60px", "80px", "100px"], 
                    flex_grow=1,
                    height="48px",
                ),
                rx.button(
                    "Mensual", size="3", 
                    color=Colors.PRIMARY.value, 
                    min_width=["60px", "80px", "100px"], 
                    flex_grow=1,
                    height="48px",
                ),
                rx.button(
                    "Anual", size="3", 
                    color=Colors.PRIMARY.value, 
                    min_width=["60px", "80px", "100px"], 
                    flex_grow=1,
                    height="48px",
                ),
                spacing="2",
                justify="center",
                width="100%",
            ),
        ),
        padding="1em",
        bg=Colors.PRIMARY.value,
        width="100vw",
        position="fixed",
        bottom=0,
        left=0,
        z_index=100,
    )

