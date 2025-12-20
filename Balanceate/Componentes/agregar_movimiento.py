import reflex as rx
from Balanceate.state import State
from Balanceate.styles.colors import Colors
from Balanceate.styles.fonts import Font, FontWeight
from Balanceate.styles.styles import Size

def agregar_movimiento() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Agregar movimiento",
            size="3",
            color="black",
            margin_bottom="5",
            font_family=Font.DEFAULT.value,
        ),

        rx.hstack(
            rx.input(
                placeholder="Nombre",
                value=State.nombre,
                on_change=State.set_nombre,
                padding="3",
                border_radius="md",
                border=f"1px solid {Colors.SECONDARY.value}",
                font_size="1rem",
                color="black",
                bg=Colors.PRIMARY.value,
                margin_right="4",
                _focus={
                    "border_color": Colors.SUCCESS.value
                },
            ),
            rx.input(
                placeholder="Valor",
                type_="number",
                value=State.valor,
                on_change=State.set_valor,
                padding="3",
                border_radius="md",
                border=f"1px solid {Colors.SECONDARY.value}",
                font_size="1rem",
                color="black",
                bg=Colors.PRIMARY.value,
                _focus={
                    "outline": f"2px solid {Colors.SUCCESS.value}",
                    "border_color": Colors.SUCCESS.value
                },
            ),

            spacing="3",
            justify="center",
            width=["87%","90%","60%"] 
        ),

        rx.hstack(
            rx.button(
                "Ingreso",
                on_click=lambda: State.agregar_movimiento("ingreso"),
                bg=Colors.SUCCESS.value,
                color="white",
                border_radius="8px",
                size="3",  
                padding="3"
            ),
            rx.button(
                "Gasto",
                on_click=lambda: State.agregar_movimiento("gasto"),
                bg=Colors.ERROR.value,
                color="white",
                border_radius="8px",
                size="3", 
                padding="3"
            ),
            spacing="4"
        ),

        spacing="4",
        align="center",
        width="100%",
        margin_bottom=Size.MEDIUM.value
    )
