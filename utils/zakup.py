from utils.db import db
import datetime

class Zamownienie():
    def __init__(self):
        self.orders = db['orders']
        self.products = db['products']


    def add_product(self, name, user_id):

        product = self.products.find_one({"name": name})

        product_id = product['_id']
        product_price = product['price']

        user_id_ = user_id

        product_name = name

        teraz_data = datetime.datetime.now()
        teraz_data = str(teraz_data)[0:22]

        self.orders.insert_one({"user_id": user_id_,
                                "created_at": teraz_data,
                                "items": [
                                    {
                                    "product_id": product_id,
                                    "quantity": 1,
                                    "price": product_price,
                                    "name": product_name
                                }],
                                "total_price": product_price,
                                "status": 'delive'}
                               )
        return product["image"], product_price, 1
    
    def expand_orders(self, _id, total_price, product_name):



        self.orders.update_one(
        {
            "_id": _id,
            "items.name": product_name
        },
        {
            "$inc": {
                "items.$.quantity": 1,  
                "total_price": total_price  
            }
        }
        )


    def check(self, name, user_id=None):
        if(user_id==None):
            print("Anonimus")
            image, price, quantity = self.add_product(name, "anonymouse")
        else:
            id_user = user_id
            product_name = name
            

            check = list(self.orders.find({"user_id": id_user, "status": "delive"}))
            
            product = list(self.products.find({"name": product_name}))
            price = 0

            for x in check:
                _id = x["_id"]
                items = x["items"]

                for item in items:
                    if item["product_id"] == product[0]["_id"]:
                        price = item["price"]

                        self.expand_orders(_id, price, product_name)
                        return product[0]["image"], price, 1
                    else:
                        continue             
            

            self.add_product(product_name, id_user)

            quantity = 1
            image = product[0]["image"]

        return image, price, quantity
        

zamowienie = Zamownienie()