from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(
    uri,
    server_api=ServerApi('1'),
    serverSelectionTimeoutMS=10000,  # 10s para detectar problemas rápido
)

db = client["balanceate"]

movimientos_collection = db["movimientos"]
usuarios_collection = db["usuarios"]
balances_collection = db["balances"]

try:
    client.admin.command('ping')
    print("✅ Conectado exitosamente a MongoDB Atlas.")
except Exception as e:
    print("❌ Error de conexión con MongoDB:", e)
