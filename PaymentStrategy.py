from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
import random

class PaymentStrategy(ABC):
    """Abstract Strategy Interface (Strategy Pattern)"""
    @abstractmethod
    def process_payment(self, amount: float, customer_info: dict) -> dict:
        pass
    
    @abstractmethod
    def validate_payment_info(self, payment_info: dict) -> bool:
        pass
    
    @abstractmethod
    def get_payment_method_name(self) -> str:
        pass

class CreditCardPayment(PaymentStrategy):
    """Concrete Strategy: Credit Card Payment"""
    def process_payment(self, amount: float, customer_info: dict) -> dict:
        # Implementation here...
        pass
    
    def validate_payment_info(self, payment_info: dict) -> bool:
        # Implementation here...
        pass
    
    def get_payment_method_name(self) -> str:
        return "Credit Card"

class VenmoPayment(PaymentStrategy):
    """Concrete Strategy: Venmo Payment"""
    def process_payment(self, amount: float, customer_info: dict) -> dict:
        # Implementation here...
        pass
    
    def validate_payment_info(self, payment_info: dict) -> bool:
        # Implementation here...
        pass
    
    def get_payment_method_name(self) -> str:
        return "Venmo"

class PayPalPayment(PaymentStrategy):
    """Concrete Strategy: PayPal Payment"""
    def process_payment(self, amount: float, customer_info: dict) -> dict:
        # Implementation here...
        pass
    
    def validate_payment_info(self, payment_info: dict) -> bool:
        # Implementation here...
        pass
    
    def get_payment_method_name(self) -> str:
        return "PayPal"