from utils.db import db
import datetime

class Koszyk():
    def __init__(self):
        self.orders = db['orders']
        self.product = db['products']

    def get_orders_by_status(self, user_id, status='delive'):
      
        query = {"user_id": user_id, "status": status}
        orders_from_db = list(self.orders.find(query))
        
        name_list = []
        price_list = []
        quantity_list = []
        image_list = []

        if not orders_from_db:
            return name_list, price_list, quantity_list, image_list
        
        for order in orders_from_db:   
            items = order.get('items', [])
            for item in items:
                product_name = item.get('name')
                product_list = self.product.find_one({"name": product_name})
                
                product_image = product_list["image"] if product_list else ""
                
                name_list.append(product_name)
                quantity_list.append(item.get('quantity', 0))
                price_list.append(item.get('price', 0))
                image_list.append(product_image)

        return name_list, price_list, quantity_list, image_list

    def not_delivered_yet(self, user_id):
        return self.get_orders_by_status(user_id, status='delive')

    def delivered_already(self, user_id):
        return self.get_orders_by_status(user_id, status='completed')

koszyk = Koszyk()