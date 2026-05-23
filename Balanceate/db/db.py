from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

_client = None
_db = None

_COLLECTION_MAP = {
    "movimientos_collection": "movimientos",
    "usuarios_collection": "usuarios",
    "balances_collection": "balances",
}


def _connect():
    global _client, _db
    if _client is None:
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise RuntimeError("MONGO_URI no está configurado en .env")
        _client = MongoClient(
            uri,
            server_api=ServerApi("1"),
            serverSelectionTimeoutMS=10000,
        )
        _db = _client["balanceate"]
        try:
            _client.admin.command("ping")
            print("✅ Conectado exitosamente a MongoDB Atlas.")
        except Exception as e:
            _client = None
            _db = None
            print("❌ Error de conexión con MongoDB:", e)
            raise
    return _db


def get_client():
    _connect()
    return _client


def get_db():
    return _connect()


def get_collection(name: str):
    return _connect()[name]


def __getattr__(name):
    if name in _COLLECTION_MAP:
        return _connect()[_COLLECTION_MAP[name]]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
