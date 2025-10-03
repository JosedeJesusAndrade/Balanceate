import reflex as rx

config = rx.Config(
    app_name="Balanceate",
    frontend_packages=[
        "react-router-dom",
    ],
    telemetry_enabled=False,
    dev_mode=True,
    routes_path="routes",
    reload_dirs=["Balanceate"]
)