"""
Main application demonstrating all three de    # Set up payment information and process payment
    order.set_payment_method("credit_card")
    order.add_payment_info({
        'card_number': '4111-1111-1111-1111',
        'expiry': '12/25',
        'cvv': '123',
        'cardholder_name': 'John Doe'
    })terns working together
"""
from config.enums import FoodCategory, OrderStatus
from config.settings import DEFAULT_RESTAURANT_NAME
from services.restaurant_service import RestaurantService
from utils.helpers import print_header, print_section_header
from view.restaurant_gui import RestaurantApp


def main():
    """Basic demonstration of the restaurant system"""
    print_header("RESTAURANT MANAGEMENT SYSTEM WITH THREE DESIGN PATTERNS")
    
    # Create restaurant
    restaurant = RestaurantService(DEFAULT_RESTAURANT_NAME)
    
    # Add staff members (observers)
    print("\n👥 Adding Staff Members...")
    chef = restaurant.add_staff_member("Chef Mario", "kitchen")
    manager = restaurant.add_staff_member("Manager Lisa", "manager")
    server = restaurant.add_staff_member("Server John", "server")
    
    # Add items to the menu using the factory pattern
    print("\n📋 Setting up menu...")
    restaurant.menu.add_item(FoodCategory.APPETIZER, "Chicken Wings", 11.99, "6 Spicy buffalo wings with blue cheese dressing")
    restaurant.menu.add_item(FoodCategory.ENTREE, "Grilled Salmon", 18.99, "Atlantic salmon with lemon herb butter")
    restaurant.menu.add_item(FoodCategory.ENTREE, "BigTown Cheeseburger", 13.99, "1/2 pound beef with lettuce, tomato")
    restaurant.menu.add_item(FoodCategory.DESSERT, "Chocolate Cake", 6.99, "Rich chocolate cake with vanilla ice cream")
    restaurant.menu.add_item(FoodCategory.BEVERAGE, "Coke", 2.49, "Classic Coca-Cola")
    
    # Display the menu
    restaurant.menu.display_menu()
    
    # Create an order
    print("\n🛒 Creating Customer Order...")
    order1 = restaurant.create_order("John Doe", "555-0123", "john@email.com")
    
    # Add items to order
    chicken_wings = restaurant.menu.get_item("Chicken Wings")
    burger = restaurant.menu.get_item("BigTown Cheeseburger")
    coke = restaurant.menu.get_item("Coke")
    
    if chicken_wings and burger and coke:
        order1.add_item(chicken_wings)
        order1.add_item(burger)
        order1.add_item(coke)
    
    # Set up payment
    order1.set_payment_method("credit_card")
    order1.add_payment_info({
        'card_number': '4111-1111-1111-1111',
        'expiry': '12/25',
        'cvv': '123',
        'cardholder_name': 'John Doe'
    })
    
    # Display order
    order1.display_order()
    
    # Process payment
    print("\n💳 Processing Payment...")
    payment_success = order1.process_payment()
    
    if payment_success:
        # Process the order through all stages
        print_header("ORDER PROCESSING WITH OBSERVER NOTIFICATIONS")
        
        order1.update_status(OrderStatus.PREPARING)
        order1.update_status(OrderStatus.READY)
        order1.update_status(OrderStatus.DELIVERED)
    
    print("\n✨ Demonstration completed!")


def strategy_pattern_payment_demo():
    """Comprehensive demonstration focusing on Strategy Pattern with payment methods"""
    print_header("BIGTOWN BISTRO: COMPLETE DESIGN PATTERNS DEMONSTRATION")
    print("Factory Pattern + Observer Pattern + Strategy Pattern")
    print("="*80)
    
    # Initialize restaurant system (Observer Pattern)
    restaurant = RestaurantService("BigTown Bistro")
    
    # Add staff members who will receive notifications
    chef = restaurant.add_staff_member("Marco", "kitchen")
    server = restaurant.add_staff_member("Sarah", "server")
    manager = restaurant.add_staff_member("David", "manager")
    cashier = restaurant.add_staff_member("Emma", "cashier")
    
    print("👥 Staff Team Assembled:")
    print("   🍳 Marco (Kitchen)")
    print("   🍽️  Sarah (Server)")
    print("   👔 David (Manager)")
    print("   💰 Emma (Cashier)")
    
    # Create orders with customer contact information (Observer Pattern)
    print_header("CREATING ORDERS (Factory Pattern)")
    
    # Setup menu items for demonstration
    restaurant.menu.add_item(FoodCategory.ENTREE, "Gourmet Burger", 15.99, "Beef patty with lettuce, tomato, and cheese")
    restaurant.menu.add_item(FoodCategory.SIDE, "Crispy Fries", 4.99, "Golden potato fries with salt")
    restaurant.menu.add_item(FoodCategory.BEVERAGE, "Coca Cola", 2.99, "Classic cola with ice")
    
    restaurant.menu.add_item(FoodCategory.ENTREE, "Margherita Pizza", 18.50, "Fresh tomato, mozzarella, and basil")
    restaurant.menu.add_item(FoodCategory.BEVERAGE, "Craft Beer", 6.99, "Local craft beer")
    
    restaurant.menu.add_item(FoodCategory.ENTREE, "Ribeye Steak", 28.99, "Premium beef with garlic and herbs")
    restaurant.menu.add_item(FoodCategory.BEVERAGE, "Red Wine", 12.99, "Rich red wine")
    restaurant.menu.add_item(FoodCategory.DESSERT, "Chocolate Cake", 7.99, "Decadent chocolate cake")
    
    # Create three different orders
    order1 = restaurant.create_order("Alice Johnson", "555-0123", "alice@email.com")
    gourmet_burger = restaurant.menu.get_item("Gourmet Burger")
    crispy_fries = restaurant.menu.get_item("Crispy Fries")
    coca_cola = restaurant.menu.get_item("Coca Cola")
    
    if gourmet_burger and crispy_fries and coca_cola:
        order1.add_item(gourmet_burger)
        order1.add_item(crispy_fries)
        order1.add_item(coca_cola)
    
    order2 = restaurant.create_order("Bob Smith", "555-0456", "bob@email.com")
    margherita_pizza = restaurant.menu.get_item("Margherita Pizza")
    craft_beer = restaurant.menu.get_item("Craft Beer")
    
    if margherita_pizza and craft_beer:
        order2.add_item(margherita_pizza)
        order2.add_item(craft_beer)
    
    order3 = restaurant.create_order("Carol Davis", "555-0789", "carol@email.com")
    ribeye_steak = restaurant.menu.get_item("Ribeye Steak")
    red_wine = restaurant.menu.get_item("Red Wine")
    chocolate_cake = restaurant.menu.get_item("Chocolate Cake")
    
    if ribeye_steak and red_wine and chocolate_cake:
        order3.add_item(ribeye_steak)
        order3.add_item(red_wine)
        order3.add_item(chocolate_cake)
    
    print("✅ Orders created using Factory Pattern for menu items")
    
    # Demonstrate Strategy Pattern with different payment methods
    print_header("STRATEGY PATTERN: PAYMENT PROCESSING")
    
    # Order 1: Credit Card Payment
    print("\n🔹 ORDER #1 - CREDIT CARD PAYMENT")
    print("-" * 40)
    order1.set_payment_method("credit_card")
    order1.add_payment_info({
        'card_number': '4111-1111-1111-1111',
        'expiry': '12/25',
        'cvv': '123',
        'cardholder_name': 'Alice Johnson'
    })
    order1.process_payment()
    order1.update_status(OrderStatus.PREPARING)
    
    # Order 2: Venmo Payment
    print("\n🔹 ORDER #2 - VENMO PAYMENT")
    print("-" * 40)
    order2.set_payment_method("venmo")
    order2.add_payment_info({
        'venmo_username': '@bob-smith',
        'phone': '555-123-0456'
    })
    order2.process_payment()
    order2.update_status(OrderStatus.PREPARING)
    
    # Order 3: PayPal Payment
    print("\n🔹 ORDER #3 - PAYPAL PAYMENT")
    print("-" * 40)
    order3.set_payment_method("paypal")
    order3.add_payment_info({
        'paypal_email': 'carol.davis@email.com'
    })
    order3.process_payment()
    order3.update_status(OrderStatus.PREPARING)
    
    # Display all orders with payment information
    print_header("FINAL ORDER STATUS WITH PAYMENT INFO")
    
    order1.display_order()
    order2.display_order()
    order3.display_order()
    
    # Complete order processing
    print_header("COMPLETING ORDER PROCESSING")
    
    print("\n🍳 Kitchen updates...")
    order1.update_status(OrderStatus.READY)
    order2.update_status(OrderStatus.READY)
    order3.update_status(OrderStatus.READY)
    
    print("\n🚚 Delivery updates...")
    order1.update_status(OrderStatus.DELIVERED)
    order2.update_status(OrderStatus.DELIVERED)
    order3.update_status(OrderStatus.DELIVERED)
    
    print_header("THREE DESIGN PATTERNS WORKING TOGETHER SUCCESSFULLY!")
    print("✅ FACTORY PATTERN: Created different types of menu items")
    print("✅ OBSERVER PATTERN: Notified customers and staff of events")
    print("✅ STRATEGY PATTERN: Processed payments using different methods")
    print("\nThe system demonstrates how multiple design patterns can")
    print("integrate seamlessly to create a robust, flexible application!")
    print("="*80)


if __name__ == "__main__":
    app = RestaurantApp()
    app.run()
