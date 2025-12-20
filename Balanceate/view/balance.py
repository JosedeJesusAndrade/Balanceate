# balance.py
import reflex as rx
from Balanceate.styles.colors import Colors
from Balanceate.state import State
from Balanceate.styles.styles import Size 

def format_currency(amount: float) -> str:
    """Formatea un número como moneda."""
    return f"${amount:,.2f}"

def balance() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.text(
                "Balance Total:", 
                font_size=[".9rem", "1rem", "1.5rem"],  # Responsive font sizes
                font_weight="400",
                color="black",
            ),
            rx.text(
                rx.cond(
                    State.balance.total >= 0,
                    f"+${State.balance.total}",
                    f"-${abs(State.balance.total)}"
                ),
                id="total_balance",
                font_size=["2.5rem", "3rem", "3.5rem"],  # Responsive font sizes
                font_weight="bold",
                color=rx.cond(
                    State.balance.total >= 0,
                    Colors.SUCCESS.value,
                    Colors.ERROR.value
                )
            ),
            align="center",
            justify="center",
        ),
        bg="white",
        border_radius="15px",
        padding=["30px", "40px", "50px"],  # Responsive padding
        box_shadow="rgba(0, 0, 0, 0.08) 0px 4px 12px",
        text_align="center",
        width=["95%", "85%", "800px"],  # 95% en mobile, 85% en tablet, 800px en desktop
        max_width="900px",
        margin_x="auto",  # Centrado horizontal
        margin_bottom=Size.MEDIUM.value  # Espacio inferior
    )