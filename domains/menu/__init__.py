"""
Modular Menu Domain Package

This package provides a comprehensive menu management system using the Factory Pattern
for creating different types of menu items with rich metadata and functionality.

Key Components:
- MenuItemBase: Abstract base class for all menu items
- MenuItemFactory: Factory for creating specialized menu items
- MenuManager: Manages collections of menu items and operations
- Specialized Items: AppetizerItem, MainCourseItem, DessertItem, BeverageItem

Usage:
    from domains.menu import MenuItemFactory, MenuManager
    
    factory = MenuItemFactory()
    manager = MenuManager()
    
    # Create items
    appetizer = factory.create_appetizer("Buffalo Wings", "Spicy chicken wings", 12.99)
    manager.add_item(appetizer)
"""

from .base import (
    MenuItemBase,
    MenuCategory,
    DietaryRestriction,
    PreparationStyle,
    NutritionalInfo,
    MenuItemMetadata
)

from .menu_item_factory import (
    MenuItemFactory,
    AppetizerItem,
    MainCourseItem,
    DessertItem,
    BeverageItem
)

from .menu_manager import MenuManager

__all__ = [
    # Base classes and types
    'MenuItemBase',
    'MenuCategory',
    'DietaryRestriction', 
    'PreparationStyle',
    'NutritionalInfo',
    'MenuItemMetadata',
    
    # Factory and specialized items
    'MenuItemFactory',
    'AppetizerItem',
    'MainCourseItem', 
    'DessertItem',
    'BeverageItem',
    
    # Manager
    'MenuManager'
]
