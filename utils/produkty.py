from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
KEY = os.getenv("MONGO_URI")
client = MongoClient(KEY)

try:
    client.admin.command("ping")
    print("Baza otwarta")

except Exception as e:
    print(f"Baza ma problem {e}")



class Produkty():
    pass




produkty = Produkty()