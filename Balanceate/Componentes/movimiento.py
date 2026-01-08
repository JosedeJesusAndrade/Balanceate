import reflex as rx
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight

def movimiento(movement: str, name: str, date: str, value: str, tipo: str = "gasto", monto_total: float = 0.0, mensualidad: float = 0.0, plazo: int = 0) -> rx.Component:
    return rx.container(
        rx.hstack(
            # Icono (cambia según tipo)
            rx.box(
                rx.cond(
                    movement == "Ingreso",
                    rx.icon("arrow-up"),
                    rx.cond(
                        movement == "Deuda",
                        rx.icon("credit-card"),
                        rx.icon("arrow-down")
                    )
                ),
                width="44px",
                height="44px",
                border_radius="50%",
                bg=rx.cond(
                    movement == "Ingreso",
                    "#eef2ff",
                    rx.cond(
                        movement == "Deuda",
                        "#fef3c7",  # Amarillo claro para deuda
                        "#fee2e2"   # Rojo claro para gasto
                    )
                ),
                color=rx.cond(
                    movement == "Ingreso",
                    "#4f46e5",
                    rx.cond(
                        movement == "Deuda",
                        "#f59e0b",  # Amarillo para deuda
                        "#ef4444"   # Rojo para gasto
                    )
                ),
                display="flex",
                align_items="center",
                justify_content="center",
            ),

            # Texto izquierdo
            rx.vstack(
                rx.text(
                    name.capitalize(),
                    font_weight="600",
                    font_size="1rem",
                ),
                # Para deudas, mostrar mensualidad en la línea inferior
                rx.cond(
                    movement == "Deuda",
                    rx.text(
                        f"Deuda • {date} • ${mensualidad}/mes",
                        font_size="0.75rem",
                        color="gray",
                    ),
                    rx.text(
                        f"{movement} • {date}",
                        font_size="0.75rem",
                        color="gray",
                    )
                ),
                align_items="start",
                spacing="1",
            ),

            rx.spacer(),

            # Texto derecho
            rx.vstack(
                rx.text(
                    value,
                    font_weight="600",
                    color=rx.cond(
                        movement == "Ingreso",
                        "#22c55e",  # Verde para ingreso
                        rx.cond(
                            movement == "Deuda",
                            "#f59e0b",  # Amarillo para deuda
                            "#ef4444"   # Rojo para gasto
                        )
                    ),
                ),
                rx.text(
                    movement,
                    font_size="0.7rem",
                    color="gray",
                ),
                align_items="end",
                spacing="1",
            ),

            align_items="center",
        ),
        bg="white",
        padding="30px",
        border_radius="15px",
        width=["90%", "85%", "100%"],
        max_width="800px",
        margin_x="auto",
        box_shadow="rgba(0, 0, 0, 0.08) 0px 4px 12px",
    )
