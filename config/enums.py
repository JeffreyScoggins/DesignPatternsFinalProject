"""
Enumerations for the Restaurant Management System
"""
from enum import Enum

class OrderStatus(Enum):
    RECEIVED = "received"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"

class FoodCategory(Enum):
    APPETIZER = "appetizer"
    ENTREE = "entree"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SIDE = "side"
