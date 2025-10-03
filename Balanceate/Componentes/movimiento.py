import reflex as rx
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight

def movimiento(movement: str, name: str, date: str, value: str) -> rx.Component:
    return rx.container(
        rx.text(
            f"{movement} - {name} - {date} - {value}",
            font_size=["0.7rem", "0.7rem", "1rem"],  
            font_weight="600",
            color="black",
            margin_bottom="10px"
        ),
        bg=Colors.PRIMARY.value,
        padding=["20px", "30px", "40px"],  
        border_radius="15px",
        text_align="center",
        width=["90%", "700px", "800px"],  
        max_width="600px",
        margin_x="auto",  
        box_shadow="rgba(0, 0, 0, 0.1) 0px 4px 12px",
    )
