from typing import Dict, List
from MenuFactory import MenuItemFactory
from FoodCategory import FoodCategory
from MenuItem import MenuItem, Appetizer, Entree, Dessert, Beverage, Side


# Menu management class
class Menu:
    def __init__(self):

        self.mf = MenuItemFactory()
        self.items: Dict[str, MenuItem] = {}
        self.menu()
    
    def menu(self):
        items = [
    (FoodCategory.APPETIZER, "Chicken Wings", 11.99, "6 Spicy buffalo wings with blue cheese dressing, and celery sticks"),
    (FoodCategory.APPETIZER, "Bruschetta", 7.99, "Toasted bread with tomatoes, basil, and balsamic glaze"),
    (FoodCategory.APPETIZER, "Mozzarella Sticks", 6.49, "Breaded and fried mozzarella sticks with marinara sauce"),
    (FoodCategory.APPETIZER, "Stuffed Mushrooms", 8.49, "Mushrooms stuffed with cheese and herbs"),
    (FoodCategory.ENTREE, "Grilled Salmon", 18.99, "Atlantic salmon with lemon herb butter"),
    (FoodCategory.ENTREE, "BigTown Cheeseburger", 13.99, "1/2 pound beef with lettuce, tomato, on a brioche bun with fries"),
    (FoodCategory.ENTREE, "Chicken Pasta", 14.99, "Grilled chicken with creamy alfredo sauce"),
    (FoodCategory.ENTREE, "Vegetable Stir Fry", 12.99, "Mixed vegetables in a savory soy sauce with rice"),
    (FoodCategory.ENTREE, "Steak Frites", 22.99, "Grilled ribeye steak with garlic herb butter and fries"),
    (FoodCategory.ENTREE, "Spaghetti Carbonara", 15.49, "Classic Italian pasta with pancetta and parmesan cheese"),
    (FoodCategory.DESSERT, "Chocolate Cake", 6.99, "Rich chocolate cake with vanilla ice cream"),
    (FoodCategory.DESSERT, "Cheesecake", 5.99, "New York style cheesecake with berry sauce"),
    (FoodCategory.DESSERT, "Apple Pie", 4.99, "Warm apple pie with a flaky crust and cinnamon"),
    (FoodCategory.DESSERT, "Tiramisu", 7.49, "Classic Italian dessert with coffee and mascarpone cheese"),
    (FoodCategory.BEVERAGE, "Coke", 2.49, "Classic Coca-Cola"),
    (FoodCategory.BEVERAGE, "Sprite", 2.49, "Refreshing lemon-lime soda"),
    (FoodCategory.BEVERAGE, "Lemonade", 2.99, "Freshly squeezed lemonade with mint"),
    (FoodCategory.BEVERAGE, "Iced Tea", 2.99, "Refreshing iced tea with lemon"),
    (FoodCategory.BEVERAGE, "Coffee", 2.49, "Freshly brewed coffee"),
    (FoodCategory.BEVERAGE, "Fresh Orange Juice", 3.99, "Freshly squeezed orange juice"),
    (FoodCategory.SIDE, "French Fries", 4.49, "Crispy golden fries"),
    (FoodCategory.SIDE, "Onion Rings", 4.49, "Crispy onion rings with ranch dressing"),
    (FoodCategory.SIDE, "Coleslaw", 3.49, "Creamy coleslaw with cabbage and carrots"),
    (FoodCategory.SIDE, "Garden Salad", 4.99, "Mixed greens with vinaigrette"),
    (FoodCategory.SIDE, "Caesar Salad", 5.99, "Romaine lettuce with Caesar dressing, croutons, and parmesan cheese")
        ]
        
        for category, name, price, description in items:
            self.add_item(category, name, price, description)
    
    def add_item(self, category: FoodCategory, name: str, price: float, description: str = ""):
        item = MenuItemFactory.create_item(category, name, price, description)
        self.items[name] = item
    
    def get_items_by_category(self, category: FoodCategory) -> List[MenuItem]:
        return [item for item in self.items.values() if item.category == category]
    
    def get_item(self, name: str) -> MenuItem:
        return self.items.get(name)
    
    def add_item_from_user_input(self, category_input: str, name: str, price: float, description: str = ""):
        """Allow the user to add a new item to the menu via input."""
        try:
            
            category = FoodCategory[category_input] 
            name = name.strip()
            price = price.strip()
            description = description.strip()

            self.add_item(category, name, price, description)
        except KeyError:
            print("Invalid category. Please try again.")
        except ValueError:
            print("Invalid input. Please ensure price is a number.")