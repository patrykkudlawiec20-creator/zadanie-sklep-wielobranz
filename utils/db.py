from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
KEY = os.getenv("MONGO_URI")
client = MongoClient(KEY)

try:
    client.admin.command("ping")
    print("Baza danych MongoDB otwarta pomyślnie!")
except Exception as e:
    print(f"Baza ma problem z połączeniem: {e}")

db = client['Sklep_filmy']