from utils.db import db
import datetime

class Logowanie:
    def __init__(self):
        self.konta = db["users"]

    def zaloguj(self, login, haslo):     
        
    

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