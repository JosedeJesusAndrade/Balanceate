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

        # Botones para seleccionar tipo de movimiento
        rx.hstack(
            rx.button(
                "Ingreso",
                on_click=lambda: State.seleccionar_tipo("ingreso"),
                bg=rx.cond(
                    State.tipo_seleccionado == "ingreso",
                    Colors.SUCCESS.value,
                    "#d1fae5"  # Verde claro cuando no está seleccionado
                ),
                color=rx.cond(
                    State.tipo_seleccionado == "ingreso",
                    "white",
                    Colors.SUCCESS.value
                ),
                border_radius="10px",
                size="3",  
                padding="4", 
                width="120px",
                font_weight="600",
                cursor="pointer",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "all 0.2s"
                }
            ),
            rx.button(
                "Gasto",
                on_click=lambda: State.seleccionar_tipo("gasto"),
                bg=rx.cond(
                    State.tipo_seleccionado == "gasto",
                    Colors.ERROR.value,
                    "#fee2e2"  # Rojo claro cuando no está seleccionado
                ),
                color=rx.cond(
                    State.tipo_seleccionado == "gasto",
                    "white",
                    Colors.ERROR.value
                ),
                border_radius="10px",
                size="3",
                padding="4",
                width="120px",
                font_weight="600",
                cursor="pointer",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "all 0.2s"
                }
            ),
            rx.button(
                "Deuda",
                on_click=lambda: State.seleccionar_tipo("deuda"),
                bg=rx.cond(
                    State.tipo_seleccionado == "deuda",
                    Colors.WARNING.value,
                    "#fef3c7"  # Amarillo claro cuando no está seleccionado
                ),
                color=rx.cond(
                    State.tipo_seleccionado == "deuda",
                    "white",
                    Colors.WARNING.value
                ),
                border_radius="10px",
                size="3",
                padding="4",
                width="120px",
                font_weight="600",
                cursor="pointer",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "all 0.2s"
                }
            ),
            spacing="4",
            justify="center"
        ),

        # Formulario dinámico para Ingreso/Gasto
        rx.cond(
            (State.tipo_seleccionado == "ingreso") | (State.tipo_seleccionado == "gasto"),
            rx.vstack(
                # Campo Nombre
                rx.text(
                    "Nombre del movimiento",
                    font_size="0.9rem",
                    font_weight="600",
                    color="#374151",
                    margin_bottom="1px",
                    text_align="left",
                    width="100%"
                ),
                rx.input(
                    placeholder="Ej: Salario, Cena, Transporte",
                    value=State.nombre,
                    on_change=State.set_nombre,
                    padding="3",
                    border_radius="md",
                    border=f"1px solid {Colors.SECONDARY.value}",
                    font_size="1rem",
                    color="black",
                    bg=Colors.PRIMARY.value,
                    width="100%",
                    _focus={
                        "border_color": Colors.SUCCESS.value
                    },
                ),
                # Campo Valor
                rx.text(
                    "Valor",
                    font_size="0.9rem",
                    font_weight="600",
                    color="#374151",
                    margin_top="10px",
                    margin_bottom="1px",
                    text_align="left",
                    width="100%"
                ),
                rx.input(
                    placeholder="Cantidad en dólares",
                    type_="number",
                    value=State.valor,
                    on_change=State.set_valor,
                    padding="3",
                    border_radius="md",
                    border=f"1px solid {Colors.SECONDARY.value}",
                    font_size="1rem",
                    color="black",
                    bg=Colors.PRIMARY.value,
                    width="100%",
                    _focus={
                        "outline": f"2px solid {Colors.SUCCESS.value}",
                        "border_color": Colors.SUCCESS.value
                    },
                ),
                rx.button(
                    rx.cond(
                        State.tipo_seleccionado == "ingreso",
                        "Agregar Ingreso",
                        "Agregar Gasto"
                    ),
                    on_click=lambda: State.agregar_movimiento(State.tipo_seleccionado),
                    bg=rx.cond(
                        State.tipo_seleccionado == "ingreso",
                        Colors.SUCCESS.value,
                        Colors.ERROR.value
                    ),
                    color="white",
                    border_radius="8px",
                    size="3",
                    padding="3",
                    width="100%",
                    font_weight="600",
                    cursor="pointer"
                ),
                spacing="3",
                width=["90%", "85%", "400px"],
                padding="4",
                bg="#f9fafb",
                border_radius="12px",
                margin_top="3"
            ),
            rx.box()  # Espacio vacío cuando no hay tipo seleccionado
        ),

        # Formulario dinámico para Deuda
        rx.cond(
            State.tipo_seleccionado == "deuda",
            rx.vstack(
                # Campo Nombre
                rx.text(
                    "Nombre de la deuda",
                    font_size="0.9rem",
                    font_weight="600",
                    color="#374151",
                    margin_bottom="1px",
                    text_align="left",
                    width="100%"
                ),
                rx.input(
                    placeholder="Ej: Préstamo personal, Tarjeta de crédito",
                    value=State.nombre,
                    on_change=State.set_nombre,
                    padding="3",
                    border_radius="md",
                    border=f"1px solid {Colors.SECONDARY.value}",
                    font_size="1rem",
                    color="black",
                    bg=Colors.PRIMARY.value,
                    width="100%",
                    _focus={
                        "border_color": Colors.WARNING.value
                    },
                ),
                # Campo Monto Total
                rx.text(
                    "Monto total",
                    font_size="0.9rem",
                    font_weight="600",
                    color="#374151",
                    margin_top="10px",
                    margin_bottom="1px",
                    text_align="left",
                    width="100%"
                ),
                rx.input(
                    placeholder="Cantidad total adeudada",
                    type_="number",
                    value=State.monto_total,
                    on_change=State.set_monto_total,
                    padding="3",
                    border_radius="md",
                    border=f"1px solid {Colors.SECONDARY.value}",
                    font_size="1rem",
                    color="black",
                    bg=Colors.PRIMARY.value,
                    width="100%",
                    _focus={
                        "border_color": Colors.WARNING.value
                    },
                ),
                # Campo Mensualidad
                rx.text(
                    "Pago mensual",
                    font_size="0.9rem",
                    font_weight="600",
                    color="#374151",
                    margin_top="10px",
                    margin_bottom="1px",
                    text_align="left",
                    width="100%"
                ),
                rx.input(
                    placeholder="Cuota mensual a pagar",
                    type_="number",
                    value=State.mensualidad,
                    on_change=State.set_mensualidad,
                    padding="3",
                    border_radius="md",
                    border=f"1px solid {Colors.SECONDARY.value}",
                    font_size="1rem",
                    color="black",
                    bg=Colors.PRIMARY.value,
                    width="100%",
                    _focus={
                        "border_color": Colors.WARNING.value
                    },
                ),
                # Campo Plazo
                rx.text(
                    "Plazo",
                    font_size="0.9rem",
                    font_weight="600",
                    color="#374151",
                    margin_top="10px",
                    margin_bottom="1px",
                    text_align="left",
                    width="100%"
                ),
                rx.input(
                    placeholder="Número de meses",
                    type_="number",
                    value=State.plazo,
                    on_change=State.set_plazo,
                    padding="3",
                    border_radius="md",
                    border=f"1px solid {Colors.SECONDARY.value}",
                    font_size="1rem",
                    color="black",
                    bg=Colors.PRIMARY.value,
                    width="100%",
                    _focus={
                        "border_color": Colors.WARNING.value
                    },
                ),
                rx.button(
                    "Agregar Deuda",
                    on_click=lambda: State.agregar_movimiento("deuda"),
                    bg=Colors.WARNING.value,
                    color="white",
                    border_radius="8px",
                    size="3",
                    padding="3",
                    width="100%",
                    font_weight="600",
                    cursor="pointer"
                ),
                spacing="3",
                width=["90%", "85%", "400px"],
                padding="4",
                bg="#f9fafb",
                border_radius="12px",
                margin_top="3"
            ),
            rx.box()  # Espacio vacío cuando no es deuda
        ),

        spacing="4",
        align="center",
        width="100%",
        margin_bottom=Size.MEDIUM.value
    )
