"""
Base Menu System Interfaces and Types
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from config.enums import FoodCategory


class MenuCategory(Enum):
    """Extended menu categories with more granular classification"""
    APPETIZER = "appetizer"
    ENTREE = "entree"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SIDE = "side"
    SOUP = "soup"
    SALAD = "salad"
    PIZZA = "pizza"
    SANDWICH = "sandwich"
    PASTA = "pasta"


class PreparationStyle(Enum):
    """Cooking/preparation methods"""
    GRILLED = "grilled"
    FRIED = "fried"
    BAKED = "baked"
    STEAMED = "steamed"
    RAW = "raw"
    MIXED = "mixed"
    BREWED = "brewed"
    CHILLED = "chilled"


class DietaryRestriction(Enum):
    """Dietary restrictions and preferences"""
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    KETO = "keto"
    LOW_CARB = "low_carb"
    HALAL = "halal"
    KOSHER = "kosher"


@dataclass
class NutritionalInfo:
    """Nutritional information for menu items"""
    calories: Optional[int] = None
    protein_grams: Optional[float] = None
    carbs_grams: Optional[float] = None
    fat_grams: Optional[float] = None
    fiber_grams: Optional[float] = None
    sodium_mg: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            'calories': self.calories,
            'protein_grams': self.protein_grams,
            'carbs_grams': self.carbs_grams,
            'fat_grams': self.fat_grams,
            'fiber_grams': self.fiber_grams,
            'sodium_mg': self.sodium_mg
        }


@dataclass
class MenuItemMetadata:
    """Extended metadata for menu items"""
    chef_special: bool = False
    seasonal: bool = False
    spice_level: int = 0  # 0-5 scale
    preparation_style: Optional[PreparationStyle] = None
    dietary_restrictions: Optional[List[DietaryRestriction]] = None
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    origin: Optional[str] = None  # e.g., "Italian", "Mexican"
    
    def __post_init__(self):
        if self.dietary_restrictions is None:
            self.dietary_restrictions = []
        if self.ingredients is None:
            self.ingredients = []
        if self.allergens is None:
            self.allergens = []


class MenuItemBase(ABC):
    """
    Enhanced Abstract Base Class for Menu Items
    
    Provides a rich interface for menu items with nutritional info,
    dietary restrictions, preparation details, and more.
    """
    
    def __init__(self, 
                 name: str, 
                 price: float, 
                 description: str = "",
                 nutritional_info: Optional[NutritionalInfo] = None,
                 metadata: Optional[MenuItemMetadata] = None):
        self.name = name
        self.price = price
        self.description = description
        self.nutritional_info = nutritional_info or NutritionalInfo()
        self.metadata = metadata or MenuItemMetadata()
        self.category: Optional[FoodCategory] = None
        self.created_at = datetime.now()
        self.available = True
    
    @abstractmethod
    def prepare(self) -> str:
        """Prepare the menu item"""
        pass
    
    @abstractmethod
    def get_preparation_time(self) -> int:
        """Get preparation time in minutes"""
        pass
    
    @abstractmethod
    def get_category(self) -> FoodCategory:
        """Get the food category for this item"""
        pass
    
    def get_display_name(self) -> str:
        """Get formatted display name with special indicators"""
        name = self.name
        restrictions = self.metadata.dietary_restrictions or []
        
        if self.metadata.chef_special:
            name += " ⭐"
        if self.metadata.seasonal:
            name += " 🍂"
        if DietaryRestriction.VEGAN in restrictions:
            name += " 🌱"
        elif DietaryRestriction.VEGETARIAN in restrictions:
            name += " 🥬"
        if DietaryRestriction.GLUTEN_FREE in restrictions:
            name += " GF"
        return name
    
    def get_spice_indicator(self) -> str:
        """Get spice level indicator"""
        if self.metadata.spice_level == 0:
            return ""
        return "🌶️" * min(self.metadata.spice_level, 5)
    
    def matches_dietary_restriction(self, restriction: DietaryRestriction) -> bool:
        """Check if item meets dietary restriction"""
        restrictions = self.metadata.dietary_restrictions or []
        return restriction in restrictions
    
    def has_allergen(self, allergen: str) -> bool:
        """Check if item contains specific allergen"""
        allergens = self.metadata.allergens or []
        return allergen.lower() in [a.lower() for a in allergens]
    
    def get_nutritional_summary(self) -> str:
        """Get formatted nutritional summary"""
        if not self.nutritional_info.calories:
            return "Nutritional info not available"
        
        return f"{self.nutritional_info.calories} cal"
    
    def set_availability(self, available: bool) -> None:
        """Set item availability"""
        self.available = available
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert menu item to dictionary"""
        restrictions = self.metadata.dietary_restrictions or []
        allergens = self.metadata.allergens or []
        
        return {
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category': self.category.value if self.category else None,
            'available': self.available,
            'chef_special': self.metadata.chef_special,
            'seasonal': self.metadata.seasonal,
            'spice_level': self.metadata.spice_level,
            'dietary_restrictions': [d.value for d in restrictions],
            'allergens': list(allergens),
            'nutritional_info': self.nutritional_info.to_dict(),
            'preparation_time': self.get_preparation_time(),
            'created_at': self.created_at.isoformat()
        }
    
    def __str__(self) -> str:
        """String representation with enhanced formatting"""
        price_str = f"${self.price:.2f}"
        spice = self.get_spice_indicator()
        nutrition = self.get_nutritional_summary()
        
        base_str = f"{self.get_display_name()} - {price_str}"
        if spice:
            base_str += f" {spice}"
        if nutrition != "Nutritional info not available":
            base_str += f" ({nutrition})"
        if self.description:
            base_str += f": {self.description}"
        if not self.available:
            base_str += " [UNAVAILABLE]"
        
        return base_str
    
    def __eq__(self, other) -> bool:
        """Equality comparison based on name and category"""
        if not isinstance(other, MenuItemBase):
            return False
        return self.name == other.name and self.category == other.category
    
    def __hash__(self) -> int:
        """Hash for use in sets and dictionaries"""
        return hash((self.name, self.category))
