from utils.db import db

class Produkty():
    def __init__(self):
        self.products = db['products']

    def show(self, category):
        
        products = list(self.products.find({"category": category}))
        for p in products:
            p['_id'] = str(p['_id'])
        return products

    def show_all(self):
        products = list(self.products.find())
        for p in products:
            p['_id'] = str(p['_id'])
        return products
    
    def show_one(self, product):

        produkt = self.products.find_one({"name": product})

        name = product
        description = 'Jakis tam bedzie opis na razie nic nie wiem. moze potem czy cos tqkiagpav0vivjiaba'
        price = produkt['price']
        active = produkt['active']
        image = produkt['image']

        return name, description, price, active, image

        
produkty = Produkty()