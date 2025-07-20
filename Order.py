from MenuFactory import MenuItem
from typing import Dict, List


class Order:
    def __init__(self, customer_name: str):
        self.customer_name = customer_name
        self.items: List[MenuItem] = []
        self.total_price = 0.0
    
    def add_item(self, item: MenuItem):
        self.items.append(item)
        self.total_price += item.price
    
    def remove_item(self, item_name: str):
        for i, item in enumerate(self.items):
            if item.name == item_name:
                self.total_price -= item.price
                self.items.pop(i)
                return True
        return False
    
    def get_total_preparation_time(self) -> int:
        return max([item.get_preparation_time() for item in self.items]) if self.items else 0
    
    def clear_order(self):
        self.items.clear()
        self.total_price = 0.0