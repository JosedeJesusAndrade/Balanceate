
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://mono:monono@cluster0.ajkdq2c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["balanceate"]  # Nombre de tu base de datos

# Colecciones de la base de datos
movimientos_collection = db["movimientos"]
usuarios_collection = db["usuarios"]
balances_collection = db["balances"]


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)