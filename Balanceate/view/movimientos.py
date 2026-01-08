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

        # Iterar sobre los grupos de movimientos
        rx.foreach(
            State.movimientos_agrupados,
            lambda grupo: rx.vstack(
                # Etiqueta del grupo (Hoy, Ayer, o fecha)
                rx.box(
                    rx.text(
                        grupo.etiqueta,
                        font_size="1rem",
                        font_weight="600",
                        color="#64748b",
                    ),
                    width="100%",
                    max_width="800px",
                    margin_x="auto",
                    padding_y="10px",
                    padding_left="20px",
                ),
                # Movimientos del grupo
                rx.foreach(
                    grupo.movimientos,
                    lambda m: movimiento(
                        movement=rx.cond(m.tipo != "", m.tipo.capitalize(), "-"),
                        name=rx.cond(m.nombre != "", m.nombre, "-"),
                        date=rx.cond(m.fecha != "", m.fecha, "-"),
                        value=rx.cond(
                            m.tipo == "ingreso",
                            f"+${m.valor}",
                            rx.cond(
                                m.tipo == "deuda",
                                f"${m.monto_total} ({m.plazo} meses)",
                                f"-${m.valor}"
                            )
                        ),
                        tipo=m.tipo,
                        monto_total=m.monto_total,
                        mensualidad=m.mensualidad,
                        plazo=m.plazo
                    )
                ),
                width="100%",
                spacing="3",
                margin_bottom="26px",
            )
        ),

        align="center",
        spacing="4",
        width=["100%", "100%", "900px"],
        max_width="900px",
        margin_x="auto",
        padding=["5px", "20px", "30px"],
        margin_y=["20px", "30px", "40px"],
        margin_bottom="100px",
    )
