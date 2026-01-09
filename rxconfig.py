import reflex as rx
import os

# Configuración de Balanceate optimizada para producción
# Refactorizado: Enero 8, 2026
# Arquitectura: Clean Architecture con Services y Repository Pattern
config = rx.Config(
    app_name="Balanceate",
    
    # Frontend
    frontend_packages=[
        "react-router-dom",
    ],
    
    # Desarrollo
    telemetry_enabled=False,
    dev_mode=True,
    reload_dirs=["Balanceate"],
    
    # Desactivar plugins problemáticos
    disable_plugins=[
        "reflex.plugins.sitemap.SitemapPlugin"
    ],
    
    # Configuración de Redis para producción
    # Timeouts aumentados para operaciones pesadas (cálculos de balance, agrupaciones)
    state_manager_redis_config={
        "lock_expiration": int(os.getenv("REFLEX_LOCK_EXPIRATION", "60000")),  # 60 segundos
        "lock_sleep": float(os.getenv("REFLEX_LOCK_SLEEP", "0.1")),
    }
)