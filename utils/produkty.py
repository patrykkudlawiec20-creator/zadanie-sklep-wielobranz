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
    def __init__(self):
        db = client["Sklep_filmy"]
        self.products = db['products']

    def show(self, category):
        categorical_products = list(self.products.find({"category": category}))

        name_list = [x['name'] for x in categorical_products]
        price_list = [y['price'] for y in categorical_products]
        link_list = [z['image'] for z in categorical_products]


        return name_list, price_list, link_list
    
    def show_all(self):

        products = list(self.products.find())
        name_list = [x['name'] for x in products]
        price_list = [y['price'] for y in products]
        link_list = [z['image'] for z in products]


        return name_list, price_list, link_list




produkty = Produkty()