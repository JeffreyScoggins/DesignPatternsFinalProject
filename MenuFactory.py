from abc import ABC, abstractmethod
from typing import Dict, List
from enum import Enum

class FoodCategory(Enum):
    APPETIZER = "appetizer"
    ENTREE = "entree"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SIDE = "side"

# Abstract base class for all menu items
class MenuItem(ABC):
    def __init__(self, name: str, price: float, description: str = ""):
        self.name = name
        self.price = price
        self.description = description
        self.category = None
    
    @abstractmethod
    def prepare(self) -> str:
        pass
    
    @abstractmethod
    def get_preparation_time(self) -> int:
        """Return preparation time in minutes"""
        pass
    
    def __str__(self):
        return f"{self.name} - ${self.price:.2f}: {self.description}"

# Concrete menu item classes
class Appetizer(MenuItem):
    def __init__(self, name: str, price: float, description: str = ""):
        super().__init__(name, price, description)
        self.category = FoodCategory.APPETIZER
    
    def prepare(self) -> str:
        return f"Preparing appetizer: {self.name}"
    
    def get_preparation_time(self) -> int:
        return 10

class Entree(MenuItem):
    def __init__(self, name: str, price: float, description: str = ""):
        super().__init__(name, price, description)
        self.category = FoodCategory.ENTREE
    
    def prepare(self) -> str:
        return f"Cooking entree: {self.name}"
    
    def get_preparation_time(self) -> int:
        return 25

class Dessert(MenuItem):
    def __init__(self, name: str, price: float, description: str = ""):
        super().__init__(name, price, description)
        self.category = FoodCategory.DESSERT
    
    def prepare(self) -> str:
        return f"Preparing dessert: {self.name}"
    
    def get_preparation_time(self) -> int:
        return 15

class Beverage(MenuItem):
    def __init__(self, name: str, price: float, description: str = ""):
        super().__init__(name, price, description)
        self.category = FoodCategory.BEVERAGE
    
    def prepare(self) -> str:
        return f"Preparing beverage: {self.name}"
    
    def get_preparation_time(self) -> int:
        return 5

class Side(MenuItem):
    def __init__(self, name: str, price: float, description: str = ""):
        super().__init__(name, price, description)
        self.category = FoodCategory.SIDE
    
    def prepare(self) -> str:
        return f"Preparing side: {self.name}"
    
    def get_preparation_time(self) -> int:
        return 8

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
        """Create a menu item based on category"""
        if category not in cls._item_classes:
            raise ValueError(f"Unknown category: {category}")
        
        item_class = cls._item_classes[category]
        return item_class(name, price, description)
    
    @classmethod
    def register_category(cls, category: FoodCategory, item_class):
        """Register a new category and its corresponding class"""
        cls._item_classes[category] = item_class
    
    @classmethod
    def get_available_categories(cls) -> List[FoodCategory]:
        """Get all available categories"""
        return list(cls._item_classes.keys())

# Menu management class
class Menu:
    def __init__(self):
        self.items: Dict[str, MenuItem] = {}
    
    def add_item(self, category: FoodCategory, name: str, price: float, description: str = ""):
        """Add an item to the menu using the factory"""
        item = MenuItemFactory.create_item(category, name, price, description)
        self.items[name] = item
        print(f"Added {item.category.value}: {item}")
    
    def remove_item(self, name: str):
        """Remove an item from the menu"""
        if name in self.items:
            del self.items[name]
            print(f"Removed {name} from menu")
        else:
            print(f"Item {name} not found in menu")
    
    def get_items_by_category(self, category: FoodCategory) -> List[MenuItem]:
        """Get all items in a specific category"""
        return [item for item in self.items.values() if item.category == category]
    
    def display_menu(self):
        """Display the entire menu organized by category"""
        print("\n" + "="*50)
        print("RESTAURANT MENU")
        print("="*50)
        
        for category in FoodCategory:
            items = self.get_items_by_category(category)
            if items:
                print(f"\n{category.value.replace('_', ' ').title()}:")
                print("-" * 30)
                for item in items:
                    print(f"  {item}")
    
    def get_item(self, name: str) -> MenuItem:
        """Get a specific item by name"""
        return self.items.get(name)

# Order class to handle customer orders
class Order:
    def __init__(self, customer_name: str):
        self.customer_name = customer_name
        self.items: List[MenuItem] = []
        self.total_price = 0.0
    
    def add_item(self, item: MenuItem):
        """Add an item to the order"""
        self.items.append(item)
        self.total_price += item.price
        print(f"Added {item.name} to order")
    
    def remove_item(self, item_name: str):
        """Remove an item from the order"""
        for i, item in enumerate(self.items):
            if item.name == item_name:
                self.total_price -= item.price
                removed_item = self.items.pop(i)
                print(f"Removed {removed_item.name} from order")
                return
        print(f"Item {item_name} not found in order")
    
    def get_total_preparation_time(self) -> int:
        """Calculate total preparation time for the order"""
        return max([item.get_preparation_time() for item in self.items]) if self.items else 0
    
    def display_order(self):
        """Display the order details"""
        print(f"\nOrder for {self.customer_name}:")
        print("-" * 30)
        for item in self.items:
            print(f"  {item.name} - ${item.price:.2f}")
        print("-" * 30)
        print(f"Total: ${self.total_price:.2f}")
        print(f"Estimated preparation time: {self.get_total_preparation_time()} minutes")

# Example usage and demonstration
def main():
    # Create a menu
    menu = Menu()
    
    # Add items to the menu using the factory pattern
    menu.add_item(FoodCategory.APPETIZER, "Chicken Wings", 11.99, "6 Spicy buffalo wings with blue cheese dressing, and celery sticks")
    menu.add_item(FoodCategory.APPETIZER, "Bruschetta", 7.99, "Toasted bread with tomatoes, basil, and balsamic glaze")
    menu.add_item(FoodCategory.APPETIZER, "Mozzarella Sticks", 6.49, "Breaded and fried mozzarella sticks with marinara sauce")
    menu.add_item(FoodCategory.APPETIZER, "Stuffed Mushrooms", 8.49, "Mushrooms stuffed with cheese and herbs")
    
    menu.add_item(FoodCategory.ENTREE, "Grilled Salmon", 18.99, "Atlantic salmon with lemon herb butter")
    menu.add_item(FoodCategory.ENTREE, "BigTown Cheeseburger", 13.99, "1/2 pound beef with lettuce, tomato, on a brioche bun with fries")
    menu.add_item(FoodCategory.ENTREE, "Chicken Pasta", 14.99, "Grilled chicken with creamy alfredo sauce")
    menu.add_item(FoodCategory.ENTREE, "Vegetable Stir Fry", 12.99, "Mixed vegetables in a savory soy sauce with rice")
    menu.add_item(FoodCategory.ENTREE, "Steak Frites", 22.99, "Grilled ribeye steak with garlic herb butter and fries")
    menu.add_item(FoodCategory.ENTREE, "Spaghetti Carbonara", 15.49, "Classic Italian pasta with pancetta and parmesan cheese")

    menu.add_item(FoodCategory.DESSERT, "Chocolate Cake", 6.99, "Rich chocolate cake with vanilla ice cream")
    menu.add_item(FoodCategory.DESSERT, "Cheesecake", 5.99, "New York style cheesecake with berry sauce")
    menu.add_item(FoodCategory.DESSERT, "Apple Pie", 4.99, "Warm apple pie with a flaky crust and cinnamon")
    menu.add_item(FoodCategory.DESSERT, "Tiramisu", 7.49, "Classic Italian dessert with coffee and mascarpone cheese")
    
    menu.add_item(FoodCategory.BEVERAGE, "Coke", 2.49, "Classic Coca-Cola")
    menu.add_item(FoodCategory.BEVERAGE, "Sprite", 2.49, "Refreshing lemon-lime soda")
    menu.add_item(FoodCategory.BEVERAGE, "Lemonade", 2.99, "Freshly squeezed lemonade with mint")
    menu.add_item(FoodCategory.BEVERAGE, "Iced Tea", 2.99, "Refreshing iced tea with lemon")
    menu.add_item(FoodCategory.BEVERAGE, "Coffee", 2.49, "Freshly brewed coffee")
    menu.add_item(FoodCategory.BEVERAGE, "Fresh Orange Juice", 3.99, "Freshly squeezed orange juice")
    
    menu.add_item(FoodCategory.SIDE, "French Fries", 4.49, "Crispy golden fries")
    menu.add_item(FoodCategory.SIDE, "Onion Rings", 4.49, "Crispy onion rings with ranch dressing")
    menu.add_item(FoodCategory.SIDE, "Coleslaw", 3.49, "Creamy coleslaw with cabbage and carrots")
    menu.add_item(FoodCategory.SIDE, "Garden Salad", 4.99, "Mixed greens with vinaigrette")
    menu.add_item(FoodCategory.SIDE, "Caesar Salad", 5.99, "Romaine lettuce with Caesar dressing, croutons, and parmesan cheese")

    
    # Display the menu
    menu.display_menu()
    
    # Create an order
    order = Order("John Doe")
    
    # Add items to the order
    chicken_wings = menu.get_item("Chicken Wings")
    beef_burger = menu.get_item("BigTown Cheeseburger")
    chocolate_cake = menu.get_item("Chocolate Cake")
    coke = menu.get_item("Coke")
    
    order.add_item(chicken_wings)
    order.add_item(beef_burger)
    order.add_item(chocolate_cake)
    order.add_item(coke)
    
    # Display the order
    order.display_order()
    
    # Demonstrate preparation
    print("\nPreparing order:")
    for item in order.items:
        print(item.prepare())

if __name__ == "__main__":
    main()