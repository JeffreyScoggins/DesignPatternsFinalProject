# 🏪 Restaurant Management System - Domain-Driven Modular Architecture

A **production-ready modular** restaurant management system demonstrating how to properly structure code around **business domains** rather than design patterns. The system showcases three design patterns (**Factory**, **Observer**, **Strategy**) as **implementation details** serving the business logic.

## 🎯 **Key Principle: Business Domains First, Patterns Second**

✅ **BEST PRACTICE**: Structuring code around business domains
```
domains/
├── menu/                   # ✅ Clear: handles menu operations & item creation
│   ├── menu_item_factory.py  # Factory Pattern implementation
│   └── menu_manager.py       # Menu management logic
├── notifications/          # ✅ Clear: handles all notification types  
│   ├── notification_system.py # Observer Pattern core interfaces
│   ├── customer.py           # Customer notifications
│   ├── staff.py             # Staff notifications
│   └── promotional.py       # Promotional notifications
└── payments/              # ✅ Clear: modular payment system
    ├── base.py             # Strategy Pattern interfaces
    ├── processor.py        # Payment context class
    ├── credit_card.py      # Credit card strategy
    ├── venmo.py           # Venmo strategy
    └── paypal.py          # PayPal strategy
```

## 📁 Project Structure

```
modular_app/
├── config/                 # Configuration and constants
│   ├── enums.py           # OrderStatus, FoodCategory enums
│   └── settings.py        # Application configuration
├── core/                  # Core business logic and base classes
│   └── base_classes.py    # Abstract base classes (Subject, Observer)
├── domains/               # Business domain implementations
│   ├── menu/             # Menu management (Factory Pattern)
│   │   ├── __init__.py   # Clean public API
│   │   ├── base.py       # Menu item base classes
│   │   ├── menu_item_factory.py  # Factory Pattern implementation
│   │   └── menu_manager.py       # Menu management logic
│   ├── notifications/    # Notification system (Observer Pattern)
│   │   ├── __init__.py   # Clean public API
│   │   ├── notification_system.py # Observer interfaces & core types
│   │   ├── customer.py   # Customer notification strategy
│   │   ├── staff.py      # Staff notification strategy
│   │   └── promotional.py # Promotional notification strategy
│   └── payments/         # Payment processing (Strategy Pattern)
│       ├── __init__.py   # Clean public API
│       ├── base.py       # Payment interfaces & data types
│       ├── processor.py  # Payment context class
│       ├── credit_card.py # Credit card payment strategy
│       ├── venmo.py      # Venmo payment strategy
│       └── paypal.py     # PayPal payment strategy
├── models/               # Data models
│   └── order.py         # Order model with integrated patterns
├── services/            # Application services
│   └── restaurant_service.py  # Main restaurant management
├── utils/               # Utility functions
│   └── helpers.py       # Common helper functions
└── main.py              # Application entry point with demos
```

## 🚀 How to Run

### Run Complete Demo
```bash
python main.py
```

### What You'll See
- **Factory Pattern**: Different menu item types (AppetizerItem, MainCourseItem, DessertItem, BeverageItem)
- **Observer Pattern**: Real-time multi-channel notifications to customers and staff
- **Strategy Pattern**: Three payment methods with full validation
  - 💳 **Credit Card**: Luhn algorithm validation, fee calculation
  - 📱 **Venmo**: Username validation, USD-only transactions  
  - 💙 **PayPal**: Email validation, multi-currency support

## 🎯 Design Patterns Demonstrated

### 1. **Factory Pattern** (Menu Management)
- **Location**: `domains/menu/menu_item_factory.py`
- **Purpose**: Create specialized menu items based on food category
- **Implementation**: 
  - `MenuItemFactory` with category-specific creation methods
  - Specialized item classes: `AppetizerItem`, `MainCourseItem`, `DessertItem`, `BeverageItem`
  - Enhanced features: preparation time, dietary preferences, temperature settings
- **Benefits**: Easy to add new food categories and item types without changing existing code

### 2. **Observer Pattern** (Notifications) 
- **Location**: `domains/notifications/`
- **Purpose**: Multi-channel notification system for order events
- **Implementation**:
  - **Core System**: `notification_system.py` with Observer interfaces
  - **Customer Notifications**: Order status updates via SMS/Email
  - **Staff Notifications**: Role-based alerts (kitchen, server, manager, cashier)
  - **Promotional**: Marketing emails with preference filtering
- **Features**: 6 notification channels (SMS, Email, Slack, Push, In-App, Webhook)
- **Benefits**: Decoupled notification logic, template-based messaging, delivery tracking

### 3. **Strategy Pattern** (Payment Processing)
- **Location**: `domains/payments/`
- **Purpose**: Support multiple payment methods interchangeably
- **Implementation**:
  - **Context**: `PaymentProcessor` manages strategy switching
  - **Strategies**: `CreditCardPayment`, `VenmoPayment`, `PayPalPayment`
  - **Validation**: Payment-specific rules and security checks
- **Features**: Runtime strategy switching, fee calculation, currency support
- **Benefits**: Easy to add new payment methods, isolated payment logic, type-safe results

## 🏗️ Architecture Benefits

- **🔧 Maintainability**: Each domain has clear responsibilities and boundaries
- **📈 Scalability**: Easy to add new features within existing domains
- **🧪 Testability**: Individual domains can be tested in isolation
- **🛡️ Type Safety**: Full type hints and validation throughout
- **🔒 Security**: Automatic data sanitization, masking, and validation
- **🚀 Production Ready**: Error handling, logging, audit trails, and delivery tracking

## 📊 Key Features

- ✅ **Multi-Channel Notifications**: SMS, Email, Slack, Push notifications with role-based filtering
- ✅ **Type-Safe Payment Results**: Structured `PaymentResult` objects with transaction details
- ✅ **Advanced Validation**: Luhn algorithm for cards, email format checking, phone validation
- ✅ **Security**: Payment data sanitization, card masking, secure processing simulation
- ✅ **Business Logic**: Payment method-specific fees, currency support, processing rules
- ✅ **Template-Based Messaging**: Professional notification formatting with personalization
- ✅ **Enhanced Menu System**: Dynamic item creation with dietary preferences and preparation times
- ✅ **Observer History**: Notification delivery tracking and failure handling
- ✅ **Strategy Flexibility**: Runtime payment method switching with validation

## 🔗 Design Pattern Integration

The three patterns work seamlessly together:

1. **Factory Pattern** creates menu items when building orders
2. **Observer Pattern** notifies stakeholders of order status changes and payment events  
3. **Strategy Pattern** processes payments using the selected payment method

**Example Flow:**
```python
# Factory Pattern: Create menu items
burger = menu_factory.create_main_course("Burger", 15.99, "Beef patty with toppings")

# Observer Pattern: Order automatically notifies observers
order.add_item(burger)  # Triggers "order_received" notification

# Strategy Pattern: Process payment with selected method
order.set_payment_method("credit_card")
order.process_payment()  # Triggers "payment_successful" notification
```

This architecture demonstrates how design patterns can be used as **implementation tools** to serve business requirements, rather than driving the code structure.

## 🚦 Recent Improvements

### ✅ **Fully Modularized Architecture** 
- Transformed from monolithic pattern files to domain-driven packages
- Each pattern now lives in its dedicated domain with clean boundaries
- Enhanced separation of concerns and maintainability

### ✅ **Enhanced Notification System**
- Renamed `base.py` → `notification_system.py` for better clarity
- Multi-channel delivery simulation with realistic success rates
- Template-based messaging with personalization
- Delivery history tracking and error handling

### ✅ **Robust Payment Processing**
- Fixed payment validation with proper test card numbers
- Luhn algorithm validation for credit cards  
- Phone number format validation for Venmo
- Email format validation for PayPal
- All payment methods now working with successful transaction processing

### ✅ **Improved Naming Conventions**
- `factory.py` → `menu_item_factory.py` for better descriptiveness
- `base.py` → `notification_system.py` for clarity
- More descriptive file names throughout the codebase

### ✅ **Production-Ready Features**
- Type-safe payment results with structured data
- Comprehensive error handling and validation
- Security features: card masking, data sanitization
- Business logic: processing fees, currency support
- Audit trails and delivery tracking

## 🔧 Dependencies

The modular architecture has clean dependency management:

```
main.py → services/restaurant_service.py
restaurant_service.py → domains/{menu,notifications,payments}/
order.py → domains/{notifications,payments}/
domains/menu/ → core/base_classes.py
domains/notifications/ → core/base_classes.py  
domains/payments/ → (self-contained)
```

## 🧪 Testing the System

Run the application to see all patterns working together:

```bash
# Full demonstration with both basic and comprehensive demos
python main.py

# Expected output:
# - Menu creation using Factory Pattern
# - Order processing with Observer notifications  
# - Payment processing with Strategy Pattern
# - Multi-channel notifications to customers and staff
# - Complete order lifecycle from creation to delivery
```
