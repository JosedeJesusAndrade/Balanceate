import reflex as rx
import os

# Configuración optimizada para Reflex 0.8.16 con soporte para producción
config = rx.Config(
    app_name="Balanceate",
    frontend_packages=[
        "react-router-dom",
    ],
    telemetry_enabled=False,
    dev_mode=True,
    reload_dirs=["Balanceate"],
    # Desactivar plugins problemáticos
    disable_plugins=[
        "reflex.plugins.sitemap.SitemapPlugin"
    ],
    # Configuración para producción - Redis con timeouts aumentados
    state_manager_redis_config={
        "lock_expiration": int(os.getenv("REFLEX_LOCK_EXPIRATION", "60000")),  # 60 segundos por defecto
        "lock_sleep": float(os.getenv("REFLEX_LOCK_SLEEP", "0.1")),
    }
)