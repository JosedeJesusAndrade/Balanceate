import reflex as rx
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight

def movimiento(movement: str, name: str, date: str, value: str) -> rx.Component:
    return rx.container(
        rx.hstack(
            # Icono (cambia según tipo)
            rx.box(
                rx.cond(
                    movement == "Ingreso",
                    rx.icon("arrow-up"),
                    rx.icon("arrow-down")
                ),
                width="44px",
                height="44px",
                border_radius="50%",  # Esto lo hace circular
                bg="#eef2ff",
                color="#4f46e5",
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
                rx.text(
                    f"{movement} • {date}",
                    font_size="0.75rem",
                    color="gray",
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
                        "#ef4444"   # Rojo para gasto
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
        padding="30px",  # Aumentado de 16px a 20px (+25%)
        border_radius="15px",
        width=["90%", "85%", "100%"],  # 90% en móvil, 85% en tablet, 100% en desktop
        max_width="800px",
        margin_x="auto",
        box_shadow="rgba(0, 0, 0, 0.08) 0px 4px 12px",
    )
