import reflex as rx
from Balanceate.state import State
from Balanceate.Componentes.movimiento import movimiento

def movimientos() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Movimientos",
            font_size=["1.2rem", "1.5rem", "2rem"],
            font_weight="bold",
            color="black",
            margin_bottom="20px"
        ),

        rx.foreach(
            State.movimientos,
            lambda m: movimiento(
                movement=rx.cond(m.tipo != "", m.tipo.capitalize(), "-"),
                name=rx.cond(m.nombre != "", m.nombre, "-"),
                date=rx.cond(m.fecha != "", m.fecha, "-"),
                value=rx.cond(
                    m.tipo == "ingreso",
                    f"+${m.valor}",
                    f"-${m.valor}"
                )
            )
        ),

        align="center",
        spacing="4",
        width=["100%", "90%", "800px"],
        max_width="900px",
        margin_x="auto",
        padding=["15px", "20px", "30px"],
        margin_y=["20px", "30px", "40px"],
        margin_bottom="100px",
    )
