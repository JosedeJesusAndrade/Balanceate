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

        # Iteramos sobre cada grupo de fecha
        rx.foreach(
            State.movimientos_agrupados,
            lambda grupo: rx.vstack(
                # Separador con la etiqueta de fecha
                rx.box(
                    rx.text(
                        grupo[0],  # "Hoy", "Ayer" o fecha
                        font_size="0.9rem",
                        font_weight="600",
                        color="gray",
                    ),
                    width="100%",
                    max_width="600px",
                    margin_x="auto",
                    margin_top="20px",
                    margin_bottom="10px",
                    padding_left="5px",
                ),
                # Movimientos de ese grupo
                rx.foreach(
                    grupo[1],
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
                width="100%",
                spacing="3",
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
