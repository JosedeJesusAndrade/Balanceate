import reflex as rx
from Balanceate.state import State

# Estado de prueba que utiliza las funcionalidades de State
class TestState(State):
    """Estado de prueba que extiende State para validar localStorage."""
    test_input: str = ""
    
    def set_test_input(self, value: str):
        """Actualiza el valor del input de prueba."""
        self.test_input = value
        
    def clear_test_data(self):
        """Limpia los datos de localStorage."""
        self.auth_token = ""
        self.test_input = ""

def test_localstorage_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "🧪 Prueba de LocalStorage - Reflex 0.8.16",
                size="6",
                margin_bottom="4"
            ),
            
            # Información del usuario actual
            rx.cond(
                TestState.usuario_actual,
                rx.box(
                    rx.text(
                        "👤 Usuario Logueado:",
                        font_weight="bold",
                        margin_bottom="2"
                    ),
                    rx.text("Nombre: ", TestState.usuario_actual.nombre, display="inline"),
                    rx.text("Email: ", TestState.usuario_actual.email, display="inline"),
                    rx.text("ID: ", TestState.usuario_actual.id, display="inline"),
                    padding="3",
                    bg="green.100",
                    border_radius="md",
                    width="100%",
                    margin_bottom="4"
                ),
                rx.box(
                    rx.text("❌ No hay usuario logueado"),
                    padding="3",
                    bg="red.100",
                    border_radius="md",
                    width="100%",
                    margin_bottom="4"
                )
            ),
            
            # Mostrar valor actual del auth_token
            rx.box(
                rx.text(
                    "🔑 Token JWT en localStorage:",
                    font_weight="bold",
                    margin_bottom="2"
                ),
                rx.cond(
                    TestState.auth_token,
                    rx.code(
                        TestState.auth_token,
                        padding="2",
                        bg="gray.100",
                        border_radius="md",
                        width="100%",
                        font_size="sm",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap"
                    ),
                    rx.code(
                        "VACÍO",
                        padding="2",
                        bg="gray.100",
                        border_radius="md",
                        width="100%",
                        font_size="sm"
                    )
                ),
                width="100%",
                margin_bottom="4"
            ),
            
            # Sección de acciones de prueba
            rx.box(
                rx.text(
                    "🔧 Acciones de Prueba:",
                    font_weight="bold",
                    margin_bottom="3"
                ),
                
                # Input para escribir nuevo valor
                rx.input(
                    placeholder="Escribe un token de prueba...",
                    value=TestState.test_input,
                    on_change=TestState.set_test_input,
                    width="100%",
                    margin_bottom="3"
                ),
                
                rx.hstack(
                    # Botón para guardar el valor
                    rx.button(
                        "💾 Guardar Token",
                        on_click=lambda: TestState.set_auth_token(TestState.test_input),
                        bg="blue.500",
                        color="white",
                        width="100%"
                    ),
                    
                    # Botón para limpiar
                    rx.button(
                        "🗑️ Limpiar Todo", 
                        on_click=TestState.clear_test_data,
                        bg="red.500",
                        color="white",
                        width="100%"
                    ),
                    spacing="2",
                    width="100%",
                    margin_bottom="3"
                ),
                
                # Botón para logout
                rx.button(
                    "🚪 Cerrar Sesión",
                    on_click=TestState.logout,
                    bg="orange.500",
                    color="white",
                    width="100%",
                    margin_bottom="3"
                ),
                
                width="100%",
                margin_bottom="4"
            ),
            
            # Instrucciones mejoradas
            rx.box(
                rx.text(
                    "📋 Pruebas de Persistencia - Reflex 0.8.16:",
                    font_weight="bold",
                    margin_bottom="3"
                ),
                
                rx.vstack(
                    rx.text("✅ Prueba 1: Persistencia básica"),
                    rx.text("   • Escribe algo en el input y guarda"),
                    rx.text("   • Refresca la página (F5) → debe persistir"),
                    
                    rx.text("✅ Prueba 2: Nueva pestaña"),
                    rx.text("   • Abre nueva pestaña y ve a /prueba"),
                    rx.text("   • Debe mostrar el mismo valor"),
                    
                    rx.text("✅ Prueba 3: Sesión real"),
                    rx.text("   • Ve a / y haz login"),
                    rx.text("   • Vuelve a /prueba → debe mostrar tu usuario"),
                    
                    rx.text("✅ Prueba 4: Logout"),
                    rx.text("   • Haz clic en 'Cerrar Sesión'"),
                    rx.text("   • localStorage debe limpiarse"),
                    
                    align_items="start",
                    spacing="1"
                ),
                
                bg="blue.50",
                border="1px solid",
                border_color="blue.200",
                padding="4",
                border_radius="md",
                width="100%"
            ),
            
            # Navegación
            rx.box(
                rx.text("🏠 ", display="inline"),
                rx.link("Volver al inicio", href="/", color="blue.500"),
                text_align="center",
                margin_top="4"
            ),
            
            width="100%",
            max_width="600px",
            spacing="4",
            padding="6"
        ),
        min_height="100vh",
        bg="gray.50"
    )