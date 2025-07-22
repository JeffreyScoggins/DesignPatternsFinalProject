"""Menu Manager - Manages collections of menu items and menu operations"""

from typing import Dict, List, Optional, Callable, Any
from .base import MenuItemBase, MenuCategory, DietaryRestriction
from .menu_item_factory import MenuItemFactory
from config.enums import FoodCategory
import logging

logger = logging.getLogger(__name__)


class MenuManager:
    """Manages menu items and provides menu operations"""
    
    def __init__(self):
        self._items: Dict[str, MenuItemBase] = {}
        self._categories: Dict[MenuCategory, List[MenuItemBase]] = {
            category: [] for category in MenuCategory
        }
        self.factory = MenuItemFactory()
    
    def add_item(self, item: MenuItemBase) -> bool:
        """Add a menu item to the menu"""
        try:
            if item.name in self._items:
                logger.warning(f"Item '{item.name}' already exists in menu")
                return False
            
            self._items[item.name] = item
            
            # Add to category list
            menu_category = self._map_food_to_menu_category(item.get_category())
            if menu_category:
                self._categories[menu_category].append(item)
            
            logger.info(f"Added menu item: {item.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding menu item: {e}")
            return False
    
    def remove_item(self, name: str) -> bool:
        """Remove a menu item from the menu"""
        try:
            if name not in self._items:
                logger.warning(f"Item '{name}' not found in menu")
                return False
            
            item = self._items[name]
            del self._items[name]
            
            # Remove from category list
            menu_category = self._map_food_to_menu_category(item.get_category())
            if menu_category and item in self._categories[menu_category]:
                self._categories[menu_category].remove(item)
            
            logger.info(f"Removed menu item: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing menu item: {e}")
            return False
    
    def get_item(self, name: str) -> Optional[MenuItemBase]:
        """Get a menu item by name"""
        return self._items.get(name)
    
    def get_all_items(self) -> List[MenuItemBase]:
        """Get all menu items"""
        return list(self._items.values())
    
    def get_items_by_category(self, category: MenuCategory) -> List[MenuItemBase]:
        """Get all items in a specific category"""
        return self._categories.get(category, [])
    
    def get_available_items(self) -> List[MenuItemBase]:
        """Get all available menu items"""
        return [item for item in self._items.values() if item.available]
    
    def get_items_by_dietary_restriction(self, restriction: DietaryRestriction) -> List[MenuItemBase]:
        """Get items that meet a specific dietary restriction"""
        return [
            item for item in self._items.values()
            if item.matches_dietary_restriction(restriction) and item.available
        ]
    
    def get_items_by_price_range(self, min_price: float, max_price: float) -> List[MenuItemBase]:
        """Get items within a specific price range"""
        return [
            item for item in self._items.values()
            if min_price <= item.price <= max_price and item.available
        ]
    
    def get_items_by_spice_level(self, max_spice_level: int) -> List[MenuItemBase]:
        """Get items with spice level at or below specified level"""
        return [
            item for item in self._items.values()
            if item.metadata.spice_level <= max_spice_level and item.available
        ]
    
    def search_items(self, query: str) -> List[MenuItemBase]:
        """Search menu items by name or description"""
        query = query.lower()
        results = []
        
        for item in self._items.values():
            if (query in item.name.lower() or 
                query in item.description.lower() or
                any(query in ingredient.lower() for ingredient in item.metadata.ingredients or [])):
                results.append(item)
        
        return results
    
    def get_chef_specials(self) -> List[MenuItemBase]:
        """Get all chef special items"""
        return [
            item for item in self._items.values()
            if item.metadata.chef_special and item.available
        ]
    
    def get_seasonal_items(self) -> List[MenuItemBase]:
        """Get all seasonal items"""
        return [
            item for item in self._items.values()
            if item.metadata.seasonal and item.available
        ]
    
    def filter_items(self, filter_func: Callable[[MenuItemBase], bool]) -> List[MenuItemBase]:
        """Filter items using a custom function"""
        return [item for item in self._items.values() if filter_func(item)]
    
    def update_item_availability(self, name: str, available: bool) -> bool:
        """Update the availability of a menu item"""
        try:
            if name not in self._items:
                logger.warning(f"Item '{name}' not found in menu")
                return False
            
            self._items[name].available = available
            logger.info(f"Updated availability for '{name}': {available}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating item availability: {e}")
            return False
    
    def update_item_price(self, name: str, new_price: float) -> bool:
        """Update the price of a menu item"""
        try:
            if name not in self._items:
                logger.warning(f"Item '{name}' not found in menu")
                return False
            
            old_price = self._items[name].price
            self._items[name].price = new_price
            logger.info(f"Updated price for '{name}': ${old_price:.2f} -> ${new_price:.2f}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating item price: {e}")
            return False
    
    def get_menu_statistics(self) -> Dict[str, Any]:
        """Get comprehensive menu statistics"""
        total_items = len(self._items)
        available_items = len(self.get_available_items())
        
        category_counts = {
            category.value: len(items) 
            for category, items in self._categories.items()
        }
        
        price_stats = self._calculate_price_statistics()
        dietary_stats = self._calculate_dietary_statistics()
        
        return {
            'total_items': total_items,
            'available_items': available_items,
            'unavailable_items': total_items - available_items,
            'category_counts': category_counts,
            'price_statistics': price_stats,
            'dietary_statistics': dietary_stats,
            'chef_specials': len(self.get_chef_specials()),
            'seasonal_items': len(self.get_seasonal_items())
        }
    
    def export_menu_data(self) -> Dict[str, Any]:
        """Export menu data for serialization"""
        return {
            'items': [item.to_dict() for item in self._items.values()],
            'statistics': self.get_menu_statistics()
        }
    
    def import_menu_data(self, menu_data: Dict[str, Any]) -> bool:
        """Import menu data from serialized format"""
        try:
            for item_data in menu_data.get('items', []):
                item = self.factory.create_from_dict(item_data)
                self.add_item(item)
            
            logger.info(f"Imported {len(menu_data.get('items', []))} menu items")
            return True
            
        except Exception as e:
            logger.error(f"Error importing menu data: {e}")
            return False
    
    def _map_food_to_menu_category(self, food_category: FoodCategory) -> Optional[MenuCategory]:
        """Map FoodCategory to MenuCategory"""
        mapping = {
            FoodCategory.APPETIZER: MenuCategory.APPETIZER,
            FoodCategory.ENTREE: MenuCategory.ENTREE,
            FoodCategory.DESSERT: MenuCategory.DESSERT,
            FoodCategory.BEVERAGE: MenuCategory.BEVERAGE,
            FoodCategory.SIDE: MenuCategory.SIDE
        }
        return mapping.get(food_category)
    
    def _calculate_price_statistics(self) -> Dict[str, float]:
        """Calculate price statistics for menu items"""
        if not self._items:
            return {}
        
        prices = [item.price for item in self._items.values()]
        
        return {
            'min_price': min(prices),
            'max_price': max(prices),
            'average_price': sum(prices) / len(prices),
            'median_price': sorted(prices)[len(prices) // 2]
        }
    
    def _calculate_dietary_statistics(self) -> Dict[str, int]:
        """Calculate dietary restriction statistics"""
        dietary_counts = {restriction.value: 0 for restriction in DietaryRestriction}
        
        for item in self._items.values():
            restrictions = item.metadata.dietary_restrictions or []
            for restriction in restrictions:
                dietary_counts[restriction.value] += 1
        
        return dietary_counts
    
    def __len__(self) -> int:
        """Return number of items in menu"""
        return len(self._items)
    
    def __contains__(self, name: str) -> bool:
        """Check if item exists in menu"""
        return name in self._items
    
    def __str__(self) -> str:
        """String representation of menu"""
        return f"MenuManager({len(self._items)} items)"
    
    def __repr__(self) -> str:
        """Detailed representation of menu"""
        stats = self.get_menu_statistics()
        return f"MenuManager(items={stats['total_items']}, available={stats['available_items']})"
