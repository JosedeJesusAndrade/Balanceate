# balance.py
import reflex as rx
from Balanceate.styles.colors import Colors
from Balanceate.state import State

def format_currency(amount: float) -> str:
    """Formatea un número como moneda."""
    return f"${amount:,.2f}"

def balance() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.text(
                "Balance Total:", 
                font_size=["1.2rem", "1.5rem", "1.8rem"],  # Responsive font sizes
                font_weight="600",
                color="black",
                margin_bottom="10px"
            ),
            rx.text(
                rx.cond(
                    State.balance.total >= 0,
                    f"+${State.balance.total}",
                    f"-${abs(State.balance.total)}"
                ),
                id="total_balance",
                font_size=["2rem", "2.5rem", "3rem"],  # Responsive font sizes
                font_weight="bold",
                color=rx.cond(
                    State.balance.total >= 0,
                    Colors.SUCCESS.value,
                    Colors.ERROR.value
                )
            ),
            spacing="2",
            align="center",
            justify="center"
        ),
        bg=Colors.PRIMARY.value,
        padding=["20px", "30px", "40px"],  # Responsive padding
        border_radius="15px",
        text_align="center",
        width=["90%", "700px", "800px"],  # Responsive width
        max_width="600px",
        margin_x="auto",  # Centrado horizontal
        box_shadow="rgba(0, 0, 0, 0.1) 0px 4px 12px",
    )