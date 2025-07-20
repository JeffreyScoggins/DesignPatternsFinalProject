from abc import ABC, abstractmethod
from FoodCategory import FoodCategory

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
        return f"{self.name} - ${self.price:.2f}"

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
        return f"Cooking main course: {self.name}"
    
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
