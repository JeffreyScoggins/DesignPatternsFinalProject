"""Menu Factory - Creates specific menu items using the Factory Pattern"""

from typing import Dict, Any, Optional, List
from decimal import Decimal
from .base import (
    MenuItemBase, MenuCategory, DietaryRestriction,
    NutritionalInfo, MenuItemMetadata, PreparationStyle
)
from config.enums import FoodCategory


class MenuItemFactory:
    """Factory for creating different types of menu items"""
    
    @staticmethod
    def create_appetizer(
        name: str,
        description: str,
        price: float,
        serving_size: Optional[str] = None,
        shareable: bool = False,
        **kwargs
    ) -> 'AppetizerItem':
        """Create an appetizer menu item"""
        return AppetizerItem(
            name=name,
            description=description,
            price=price,
            serving_size=serving_size,
            shareable=shareable,
            **kwargs
        )
    
    @staticmethod
    def create_main_course(
        name: str,
        description: str,
        price: float,
        protein_source: Optional[str] = None,
        cooking_method: Optional[str] = None,
        **kwargs
    ) -> 'MainCourseItem':
        """Create a main course menu item"""
        return MainCourseItem(
            name=name,
            description=description,
            price=price,
            protein_source=protein_source,
            cooking_method=cooking_method,
            **kwargs
        )
    
    @staticmethod
    def create_dessert(
        name: str,
        description: str,
        price: float,
        sweetness_level: str = "medium",
        temperature: str = "room",
        **kwargs
    ) -> 'DessertItem':
        """Create a dessert menu item"""
        return DessertItem(
            name=name,
            description=description,
            price=price,
            sweetness_level=sweetness_level,
            temperature=temperature,
            **kwargs
        )
    
    @staticmethod
    def create_beverage(
        name: str,
        description: str,
        price: float,
        beverage_type: str = "soft",
        temperature: str = "cold",
        caffeine_content: Optional[int] = None,
        **kwargs
    ) -> 'BeverageItem':
        """Create a beverage menu item"""
        return BeverageItem(
            name=name,
            description=description,
            price=price,
            beverage_type=beverage_type,
            temperature=temperature,
            caffeine_content=caffeine_content,
            **kwargs
        )
    
    @classmethod
    def create_from_dict(cls, item_data: Dict[str, Any]) -> MenuItemBase:
        """Create menu item from dictionary data"""
        category = item_data.get('category', 'appetizer')
        
        # Extract base parameters
        base_params = {
            'name': item_data['name'],
            'description': item_data['description'],
            'price': float(item_data['price'])
        }
        
        # Add nutritional info if present
        if 'nutritional_info' in item_data:
            nutritional_data = item_data['nutritional_info']
            base_params['nutritional_info'] = NutritionalInfo(
                calories=nutritional_data.get('calories'),
                protein_grams=nutritional_data.get('protein_grams'),
                carbs_grams=nutritional_data.get('carbs_grams'),
                fat_grams=nutritional_data.get('fat_grams'),
                fiber_grams=nutritional_data.get('fiber_grams'),
                sodium_mg=nutritional_data.get('sodium_mg')
            )
        
        # Add metadata if present
        if 'metadata' in item_data:
            metadata = item_data['metadata']
            dietary_restrictions = [
                DietaryRestriction(r) for r in metadata.get('dietary_restrictions', [])
            ]
            base_params['metadata'] = MenuItemMetadata(
                dietary_restrictions=dietary_restrictions,
                allergens=metadata.get('allergens', []),
                spice_level=metadata.get('spice_level', 0),
                preparation_style=PreparationStyle(metadata['preparation_style']) if metadata.get('preparation_style') else None,
                chef_special=metadata.get('chef_special', False),
                seasonal=metadata.get('seasonal', False)
            )
        
        # Create specific item type
        if category == MenuCategory.APPETIZER.value:
            return cls.create_appetizer(
                serving_size=item_data.get('serving_size'),
                shareable=item_data.get('shareable', False),
                **base_params
            )
        elif category == MenuCategory.ENTREE.value:
            return cls.create_main_course(
                protein_source=item_data.get('protein_source'),
                cooking_method=item_data.get('cooking_method'),
                **base_params
            )
        elif category == MenuCategory.DESSERT.value:
            return cls.create_dessert(
                sweetness_level=item_data.get('sweetness_level', 'medium'),
                temperature=item_data.get('temperature', 'room'),
                **base_params
            )
        elif category == MenuCategory.BEVERAGE.value:
            return cls.create_beverage(
                beverage_type=item_data.get('beverage_type', 'soft'),
                temperature=item_data.get('temperature', 'cold'),
                caffeine_content=item_data.get('caffeine_content'),
                **base_params
            )
        else:
            # Default to appetizer
            return cls.create_appetizer(**base_params)


class AppetizerItem(MenuItemBase):
    """Specialized appetizer menu item"""
    
    def __init__(
        self,
        serving_size: Optional[str] = None,
        shareable: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.serving_size = serving_size
        self.shareable = shareable
        self.category = FoodCategory.APPETIZER
    
    def prepare(self) -> str:
        """Prepare the appetizer"""
        return f"Preparing appetizer: {self.name}"
    
    def get_category(self) -> FoodCategory:
        """Get appetizer category"""
        return FoodCategory.APPETIZER
    
    def get_preparation_time(self) -> int:
        """Appetizers typically quick to prepare"""
        base_time = 10  # Base appetizer time
        if self.metadata.spice_level > 2:
            base_time += 2
        return max(5, base_time)
    
    def get_display_name(self) -> str:
        """Enhanced display name for appetizers"""
        base_name = super().get_display_name()
        if self.shareable:
            base_name += " (Shareable)"
        if self.serving_size:
            base_name += f" ({self.serving_size})"
        return base_name


class MainCourseItem(MenuItemBase):
    """Specialized main course menu item"""
    
    def __init__(
        self,
        protein_source: Optional[str] = None,
        cooking_method: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.protein_source = protein_source
        self.cooking_method = cooking_method
        self.category = FoodCategory.ENTREE
    
    def prepare(self) -> str:
        """Prepare the main course"""
        method = f" using {self.cooking_method}" if self.cooking_method else ""
        return f"Preparing main course: {self.name}{method}"
    
    def get_category(self) -> FoodCategory:
        """Get main course category"""
        return FoodCategory.ENTREE
    
    def get_preparation_time(self) -> int:
        """Main courses typically take longer"""
        base_time = 20
        
        # Adjust based on cooking method
        cooking_adjustments = {
            'grilled': 5,
            'fried': -2,
            'braised': 15,
            'roasted': 10,
            'steamed': -3
        }
        
        adjustment = cooking_adjustments.get(self.cooking_method, 0) if self.cooking_method else 0
        spice_adjustment = self.metadata.spice_level if self.metadata.spice_level > 3 else 0
        
        return max(10, base_time + adjustment + spice_adjustment)
    
    def get_display_name(self) -> str:
        """Enhanced display name for main courses"""
        base_name = super().get_display_name()
        if self.cooking_method and self.protein_source:
            base_name += f" ({self.cooking_method.title()} {self.protein_source.title()})"
        elif self.cooking_method:
            base_name += f" ({self.cooking_method.title()})"
        elif self.protein_source:
            base_name += f" ({self.protein_source.title()})"
        return base_name


class DessertItem(MenuItemBase):
    """Specialized dessert menu item"""
    
    def __init__(
        self,
        sweetness_level: str = "medium",
        temperature: str = "room",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.sweetness_level = sweetness_level
        self.temperature = temperature
        self.category = FoodCategory.DESSERT
    
    def prepare(self) -> str:
        """Prepare the dessert"""
        temp_desc = f" ({self.temperature})" if self.temperature != "room" else ""
        return f"Preparing dessert: {self.name}{temp_desc}"
    
    def get_category(self) -> FoodCategory:
        """Get dessert category"""
        return FoodCategory.DESSERT
    
    def get_preparation_time(self) -> int:
        """Desserts preparation time varies by temperature"""
        base_time = 8
        
        # Frozen desserts need extra time
        if self.temperature == "frozen":
            return base_time + 5
        elif self.temperature == "hot":
            return base_time + 3
        return base_time
    
    def get_display_name(self) -> str:
        """Enhanced display name for desserts"""
        base_name = super().get_display_name()
        if self.temperature != "room":
            base_name += f" ({self.temperature.title()})"
        if self.sweetness_level in ["low", "high"]:
            base_name += f" - {self.sweetness_level.title()} Sweet"
        return base_name


class BeverageItem(MenuItemBase):
    """Specialized beverage menu item"""
    
    def __init__(
        self,
        beverage_type: str = "soft",
        temperature: str = "cold",
        caffeine_content: Optional[int] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.beverage_type = beverage_type
        self.temperature = temperature
        self.caffeine_content = caffeine_content
        self.category = FoodCategory.BEVERAGE
    
    def prepare(self) -> str:
        """Prepare the beverage"""
        temp_desc = f" ({self.temperature})" if self.temperature else ""
        return f"Preparing beverage: {self.name}{temp_desc}"
    
    def get_category(self) -> FoodCategory:
        """Get beverage category"""
        return FoodCategory.BEVERAGE
    
    def get_preparation_time(self) -> int:
        """Beverages are usually quick"""
        if self.beverage_type in ["coffee", "tea", "hot"]:
            return 3
        elif self.beverage_type == "smoothie":
            return 4
        return 1  # Most beverages are immediate
    
    def is_caffeinated(self) -> bool:
        """Check if beverage contains caffeine"""
        return self.caffeine_content is not None and self.caffeine_content > 0
    
    def get_display_name(self) -> str:
        """Enhanced display name for beverages"""
        base_name = super().get_display_name()
        if self.temperature != "room" and self.temperature:
            base_name += f" ({self.temperature.title()})"
        if self.is_caffeinated():
            base_name += f" - {self.caffeine_content}mg caffeine"
        return base_name
