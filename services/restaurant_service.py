"""
Restaurant Management Service integrating all design patterns
"""
from typing import Dict, List, Optional

from core.base_classes import Subject
from domains.notifications import StaffNotifier, PromotionalSubscriber
from domains.menu import MenuManager, MenuItemFactory, MenuCategory
from models.order import Order
from config.enums import FoodCategory


class MenuWrapper:
    """Wrapper to provide backward compatibility for menu operations"""
    
    def __init__(self, menu_manager: MenuManager, factory: MenuItemFactory):
        self._manager = menu_manager
        self._factory = factory
    
    def add_item(self, category: FoodCategory, name: str, price: float, description: str = ""):
        """Backward compatible add_item method"""
        if category == FoodCategory.APPETIZER:
            item = self._factory.create_appetizer(name, description, price)
        elif category == FoodCategory.ENTREE:
            item = self._factory.create_main_course(name, description, price)
        elif category == FoodCategory.DESSERT:
            item = self._factory.create_dessert(name, description, price)
        elif category == FoodCategory.BEVERAGE:
            item = self._factory.create_beverage(name, description, price)
        else:
            # Default to appetizer for unknown categories
            item = self._factory.create_appetizer(name, description, price)
        
        self._manager.add_item(item)
        category_str = category.value if category else "Unknown Category"
        print(f"Added {category_str}: {item.get_display_name()} - ${item.price:.2f}")
    
    def display_menu(self):
        """Backward compatible display_menu method"""
        print("\n" + "="*50)
        print("RESTAURANT MENU")
        print("="*50)
        
        for category in MenuCategory:
            items = self._manager.get_items_by_category(category)
            if items:
                print(f"\n{category.value.replace('_', ' ').title()}:")
                print("-" * 30)
                for item in items:
                    print(f"  {item.get_display_name()} - ${item.price:.2f}")
                    if item.description:
                        print(f"    {item.description}")
    
    def get_item(self, name: str):
        """Get item by name"""
        return self._manager.get_item(name)
    
    def remove_item(self, name: str):
        """Remove item by name"""
        return self._manager.remove_item(name)
    
    def get_items_by_category(self, category):
        """Get items by category - maps FoodCategory to MenuCategory"""
        # Map FoodCategory to MenuCategory
        category_mapping = {
            FoodCategory.APPETIZER: MenuCategory.APPETIZER,
            FoodCategory.ENTREE: MenuCategory.ENTREE,
            FoodCategory.DESSERT: MenuCategory.DESSERT,
            FoodCategory.BEVERAGE: MenuCategory.BEVERAGE,
            FoodCategory.SIDE: MenuCategory.SIDE
        }
        menu_category = category_mapping.get(category)
        if menu_category:
            return self._manager.get_items_by_category(menu_category)
        return []


class RestaurantService(Subject):
    """Restaurant Management System with Observer Pattern"""
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self._menu_manager = MenuManager()
        self.orders: Dict[int, Order] = {}
        self.promotional_subscribers: List[PromotionalSubscriber] = []
        
        # Initialize menu factory for compatibility
        self.menu_factory = MenuItemFactory()
        
        # Create a menu wrapper for backward compatibility
        self.menu = MenuWrapper(self._menu_manager, self.menu_factory)
    
    def add_staff_member(self, staff_name: str, role: str):
        """Add a staff member who will receive notifications"""
        staff_notifier = StaffNotifier(staff_name, role)
        self.attach(staff_notifier)
        return staff_notifier
    
    def add_promotional_subscriber(self, customer_name: str, email: str, preferences: Optional[List[str]] = None):
        """Add a customer to promotional notifications"""
        if preferences is None:
            preferences = []
        subscriber = PromotionalSubscriber(customer_name, email, preferences)
        self.promotional_subscribers.append(subscriber)
        self.attach(subscriber)
        print(f"✅ {customer_name} subscribed to promotional emails")
        return subscriber
    
    def create_order(self, customer_name: str, customer_phone: str = "", customer_email: str = "") -> Order:
        """Create a new order"""
        order = Order(customer_name, customer_phone, customer_email)
        self.orders[order.order_id] = order
        
        # Attach restaurant staff to this order
        for observer in self._observers:
            if isinstance(observer, StaffNotifier):
                order.attach(observer)
        
        return order
    
    def process_order(self, order_id: int):
        """Process an order through all stages"""
        if order_id not in self.orders:
            print(f"Order #{order_id} not found")
            return
        
        order = self.orders[order_id]
        print(f"Processing order #{order_id}...")
        
        # Update through each stage
        order.update_status(order.status)  # Current status notification
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID"""
        return self.orders.get(order_id)
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        return list(self.orders.values())
    
    def get_orders_by_status(self, status) -> List[Order]:
        """Get orders by status"""
        return [order for order in self.orders.values() if order.status == status]
    
    def send_promotion(self, category: str, message: str):
        """Send promotional notification to subscribers"""
        self.notify("promotion", {"category": category, "message": message})
    
    def display_restaurant_info(self):
        """Display restaurant information"""
        print(f"\n🏪 {self.name}")
        print(f"📊 Total Orders: {len(self.orders)}")
        print(f"👥 Staff Members: {len([obs for obs in self._observers if isinstance(obs, StaffNotifier)])}")
        print(f"📧 Promotional Subscribers: {len(self.promotional_subscribers)}")
        
    def __str__(self) -> str:
        return f"Restaurant: {self.name} ({len(self.orders)} orders)"
