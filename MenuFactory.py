from typing import Dict, List
from FoodCategory import FoodCategory
from MenuItem import MenuItem, Appetizer, Entree, Dessert, Beverage, Side

# Factory class for creating menu items
class MenuItemFactory:
    _item_classes = {
        FoodCategory.APPETIZER: Appetizer,
        FoodCategory.ENTREE: Entree,
        FoodCategory.DESSERT: Dessert,
        FoodCategory.BEVERAGE: Beverage,
        FoodCategory.SIDE: Side
    }
    
    @classmethod
    def create_item(cls, category: FoodCategory, name: str, price: float, description: str = "") -> MenuItem:
        if category not in cls._item_classes:
            raise ValueError(f"Unknown category: {category}")
        
        item_class = cls._item_classes[category]
        return item_class(name, price, description)



