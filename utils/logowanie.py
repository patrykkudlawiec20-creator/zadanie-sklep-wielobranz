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


class Logowanie:
    def __init__(self):
        
        db = client["Sklep_filmy"]
        self.konta = db["users"]

    def zaloguj(self, login, haslo):     
        
        # Sprawdzenie czy konto istnieje, zalogowanie, aktualizacja ostatniej daty logowanie, stworzenie secji

        user = self.konta.find_one({"email": login})
        email = user['email']
        if not user:
            return "Zły login"
        if user["password"] == haslo:
            teraz_data = datetime.datetime.now()
            teraz_data = str(teraz_data)[0:22]
            self.konta.update_one({"_id": user['_id']},
                                  {"$set": {"last_login": teraz_data}})
            user_id = user['_id']

            return "Zalogowano pomyślnie", user_id, email
        return "Błędne hasło", 0, 0

    def zarejestruj(self, login, haslo):
        if self.konta.find_one({"email": login}):
            return "Konto już istnieje"
        
        teraz_data = datetime.datetime.now()
        teraz_data = str(teraz_data)[0:22]

        self.konta.insert_one({"email": login,
                                "password": haslo,
                                "created_at": teraz_data,
                                "last_login": teraz_data,
                                "preferences": {
                                    "favorite_categories": [],
                                    "price_range": []
                                },
                                
                                "stats": {
                                    "total_orders": 0,
                                    "total_spent": 0
                                }})
        return "Konto zostało utworzone"

logowanie = Logowanie()