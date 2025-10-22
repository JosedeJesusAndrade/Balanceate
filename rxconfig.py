import reflex as rx

import reflex as rx

# Configuración optimizada para Reflex 0.8.13
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
)