"""
Business domain modules.
Contains menu management, notification system, and payment processing.
Each module implements appropriate design patterns for its domain.
"""

from .menu import MenuItemFactory, MenuManager, AppetizerItem, MainCourseItem, DessertItem, BeverageItem
from .notifications import CustomerNotifier, StaffNotifier, PromotionalSubscriber
from .payments import PaymentProcessor, CreditCardPayment, VenmoPayment, PayPalPayment

__all__ = [
    # Menu Management (Factory Pattern)
    'MenuItemFactory',
    'MenuManager',
    'AppetizerItem',
    'MainCourseItem',
    'DessertItem', 
    'BeverageItem',
    
    # Notifications (Observer Pattern)
    'CustomerNotifier',
    'StaffNotifier', 
    'PromotionalSubscriber',
    
    # Payment Processing (Strategy Pattern)
    'PaymentProcessor',
    'CreditCardPayment',
    'VenmoPayment',
    'PayPalPayment'
]
