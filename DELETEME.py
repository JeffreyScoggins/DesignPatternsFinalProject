from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime

# Observer Pattern Implementation
class Observer(ABC):
    """Abstract observer interface"""
    @abstractmethod
    def update(self, subject, event_type: str, data: dict):
        pass

class Subject(ABC):
    """Abstract subject interface"""
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Attach an observer to the subject"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Observer {observer.__class__.__name__} attached")
    
    def detach(self, observer: Observer):
        """Detach an observer from the subject"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Observer {observer.__class__.__name__} detached")
    
    def notify(self, event_type: str, data: dict):
        """Notify all observers about an event"""
        for observer in self._observers:
            observer.update(self, event_type, data)

# Concrete Observer Classes
class CustomerNotifier(Observer):
    """Notifies customers about their order status"""
    def __init__(self, customer_name: str, phone: str = "", email: str = ""):
        self.customer_name = customer_name
        self.phone = phone
        self.email = email
    
    def update(self, subject, event_type: str, data: dict):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if event_type == "order_received":
            print(f"[{timestamp}] SMS/Email to {self.customer_name}: Your order #{data['order_id']} has been received! Total: ${data['total']:.2f}")
        elif event_type == "order_preparing":
            print(f"[{timestamp}] SMS/Email to {self.customer_name}: Your order #{data['order_id']} is now being prepared. ETA: {data['eta']} minutes")
        elif event_type == "order_ready":
            print(f"[{timestamp}] SMS/Email to {self.customer_name}: Your order #{data['order_id']} is ready for pickup/delivery!")
        elif event_type == "order_delivered":
            print(f"[{timestamp}] SMS/Email to {self.customer_name}: Your order #{data['order_id']} has been delivered. Thank you!")
        elif event_type == "payment_successful":
            print(f"[{timestamp}] SMS/Email to {self.customer_name}: Payment confirmed! ${data['amount']:.2f} via {data['payment_method']} (ID: {data['transaction_id']})")
        elif event_type == "payment_failed":
            print(f"[{timestamp}] SMS/Email to {self.customer_name}: Payment failed for order #{data['order_id']}. Please try a different payment method.")

class StaffNotifier(Observer):
    """Notifies restaurant staff about order updates"""
    def __init__(self, staff_name: str, role: str):
        self.staff_name = staff_name
        self.role = role
    
    def update(self, subject, event_type: str, data: dict):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if event_type == "order_received" and self.role in ["kitchen", "manager"]:
            print(f"[{timestamp}] STAFF ALERT ({self.staff_name} - {self.role}): New order #{data['order_id']} received - {len(data['items'])} items")
        elif event_type == "order_preparing" and self.role in ["kitchen", "server"]:
            print(f"[{timestamp}] STAFF UPDATE ({self.staff_name} - {self.role}): Order #{data['order_id']} in preparation")
        elif event_type == "order_ready" and self.role in ["server", "manager"]:
            print(f"[{timestamp}] STAFF ALERT ({self.staff_name} - {self.role}): Order #{data['order_id']} ready for service!")
        elif event_type == "payment_successful" and self.role in ["manager", "cashier"]:
            print(f"[{timestamp}] STAFF ALERT ({self.staff_name} - {self.role}): Payment received! Order #{data['order_id']} - ${data['amount']:.2f} via {data['payment_method']}")
        elif event_type == "payment_failed" and self.role in ["manager", "cashier"]:
            print(f"[{timestamp}] STAFF ALERT ({self.staff_name} - {self.role}): Payment FAILED for order #{data['order_id']} - Requires attention!")

class PromotionalSubscriber(Observer):
    """Handles promotional emails and special deals"""
    def __init__(self, customer_name: str, email: str, preferences: Optional[List[str]] = None):
        self.customer_name = customer_name
        self.email = email
        self.preferences = preferences if preferences is not None else []
    
    def update(self, subject, event_type: str, data: dict):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if event_type == "promotion":
            if not self.preferences or data['category'] in self.preferences:
                print(f"[{timestamp}] PROMO EMAIL to {self.customer_name}: {data['message']}")
        elif event_type == "loyalty_reward":
            print(f"[{timestamp}] LOYALTY EMAIL to {self.customer_name}: {data['message']}")

class PaymentStrategy(ABC):
    """
    Abstract Strategy Interface (Strategy Pattern)
    
    This defines the interface that all concrete payment strategies must implement.
    The Strategy pattern allows the payment method to be selected and changed at runtime
    without modifying the client code.
    
    Benefits:
    - Easy to add new payment methods
    - Payment logic is encapsulated in separate classes
    - Runtime selection of payment strategy
    - Follows Open/Closed Principle
    """
    
    @abstractmethod
    def process_payment(self, amount: float, customer_info: dict) -> dict:
        """
        Process payment using the specific payment method.
        
        Args:
            amount: Payment amount in dollars
            customer_info: Dictionary containing customer payment details
            
        Returns:
            Dictionary containing payment result information
        """
        pass
    
    @abstractmethod
    def validate_payment_info(self, payment_info: dict) -> bool:
        """
        Validate payment information for this payment method.
        
        Args:
            payment_info: Dictionary containing payment method specific information
            
        Returns:
            Boolean indicating if payment information is valid
        """
        pass
    
    @abstractmethod
    def get_payment_method_name(self) -> str:
        """
        Get the display name of this payment method.
        
        Returns:
            String name of the payment method
        """
        pass

class CreditCardPayment(PaymentStrategy):
    """
    Concrete Strategy: Credit Card Payment (Strategy Pattern)
    
    Implements credit card payment processing with card validation and
    secure transaction handling.
    """
    
    def process_payment(self, amount: float, customer_info: dict) -> dict:
        """
        Process credit card payment.
        
        Args:
            amount: Payment amount
            customer_info: Must contain 'card_number', 'expiry', 'cvv', 'cardholder_name'
            
        Returns:
            Payment result dictionary
        """
        print(f"💳 Processing credit card payment of ${amount:.2f}...")
        
        # Simulate credit card processing
        card_number = customer_info.get('card_number', '****-****-****-****')
        masked_card = f"****-****-****-{card_number[-4:]}" if len(card_number) >= 4 else card_number
        
        print(f"   Card: {masked_card}")
        print(f"   Cardholder: {customer_info.get('cardholder_name', 'N/A')}")
        print(f"   Processing through secure payment gateway...")
        
        # Simulate processing time and result
        import random
        success = random.random() > 0.05  # 95% success rate
        
        if success:
            transaction_id = f"CC_{random.randint(100000, 999999)}"
            print(f"   ✅ Payment successful! Transaction ID: {transaction_id}")
            
            return {
                'success': True,
                'transaction_id': transaction_id,
                'payment_method': 'Credit Card',
                'amount': amount,
                'masked_card': masked_card
            }
        else:
            print(f"   ❌ Payment failed! Please check your card information.")
            return {
                'success': False,
                'error': 'Card declined',
                'payment_method': 'Credit Card'
            }
    
    def validate_payment_info(self, payment_info: dict) -> bool:
        """Validate credit card information."""
        required_fields = ['card_number', 'expiry', 'cvv', 'cardholder_name']
        
        for field in required_fields:
            if field not in payment_info or not payment_info[field]:
                print(f"❌ Missing required field: {field}")
                return False
        
        # Basic card number validation (simplified)
        card_number = payment_info['card_number'].replace('-', '').replace(' ', '')
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            print("❌ Invalid card number format")
            return False
        
        return True
    
    def get_payment_method_name(self) -> str:
        return "Credit Card"

class VenmoPayment(PaymentStrategy):
    """
    Concrete Strategy: Venmo Payment (Strategy Pattern)
    
    Implements Venmo payment processing with username verification
    and social payment features.
    """
    
    def process_payment(self, amount: float, customer_info: dict) -> dict:
        """
        Process Venmo payment.
        
        Args:
            amount: Payment amount
            customer_info: Must contain 'venmo_username', 'phone'
            
        Returns:
            Payment result dictionary
        """
        print(f"📱 Processing Venmo payment of ${amount:.2f}...")
        
        venmo_username = customer_info.get('venmo_username', '@unknown')
        phone = customer_info.get('phone', 'N/A')
        
        print(f"   Venmo: {venmo_username}")
        print(f"   Phone: {phone}")
        print(f"   Sending payment request through Venmo API...")
        
        # Simulate Venmo processing
        import random
        success = random.random() > 0.03  # 97% success rate
        
        if success:
            transaction_id = f"VEN_{random.randint(100000, 999999)}"
            print(f"   ✅ Payment successful! Venmo Transaction ID: {transaction_id}")
            print(f"   💬 Payment note: 'Order from BigTown Bistro 🍽️'")
            
            return {
                'success': True,
                'transaction_id': transaction_id,
                'payment_method': 'Venmo',
                'amount': amount,
                'venmo_username': venmo_username
            }
        else:
            print(f"   ❌ Venmo payment failed! Please check your account.")
            return {
                'success': False,
                'error': 'Venmo transaction failed',
                'payment_method': 'Venmo'
            }
    
    def validate_payment_info(self, payment_info: dict) -> bool:
        """Validate Venmo payment information."""
        required_fields = ['venmo_username', 'phone']
        
        for field in required_fields:
            if field not in payment_info or not payment_info[field]:
                print(f"❌ Missing required field: {field}")
                return False
        
        # Validate Venmo username format
        username = payment_info['venmo_username']
        if not username.startswith('@') or len(username) < 2:
            print("❌ Invalid Venmo username format (should start with @)")
            return False
        
        return True
    
    def get_payment_method_name(self) -> str:
        return "Venmo"

class PayPalPayment(PaymentStrategy):
    """
    Concrete Strategy: PayPal Payment (Strategy Pattern)
    
    Implements PayPal payment processing with email verification
    and secure PayPal gateway integration.
    """
    
    def process_payment(self, amount: float, customer_info: dict) -> dict:
        """
        Process PayPal payment.
        
        Args:
            amount: Payment amount
            customer_info: Must contain 'paypal_email'
            
        Returns:
            Payment result dictionary
        """
        print(f"💙 Processing PayPal payment of ${amount:.2f}...")
        
        paypal_email = customer_info.get('paypal_email', 'unknown@email.com')
        
        print(f"   PayPal Email: {paypal_email}")
        print(f"   Redirecting to PayPal secure checkout...")
        
        # Simulate PayPal processing
        import random
        success = random.random() > 0.02  # 98% success rate
        
        if success:
            transaction_id = f"PP_{random.randint(100000, 999999)}"
            print(f"   ✅ PayPal payment successful! Transaction ID: {transaction_id}")
            print(f"   🔒 Payment processed securely through PayPal")
            
            return {
                'success': True,
                'transaction_id': transaction_id,
                'payment_method': 'PayPal',
                'amount': amount,
                'paypal_email': paypal_email
            }
        else:
            print(f"   ❌ PayPal payment failed! Please try again.")
            return {
                'success': False,
                'error': 'PayPal transaction failed',
                'payment_method': 'PayPal'
            }
    
    def validate_payment_info(self, payment_info: dict) -> bool:
        """Validate PayPal payment information."""
        if 'paypal_email' not in payment_info or not payment_info['paypal_email']:
            print("❌ Missing PayPal email address")
            return False
        
        # Basic email validation
        email = payment_info['paypal_email']
        if '@' not in email or '.' not in email:
            print("❌ Invalid email format")
            return False
        
        return True
    
    def get_payment_method_name(self) -> str:
        return "PayPal"

class PaymentProcessor:
    
    def __init__(self, payment_strategy: Optional[PaymentStrategy] = None):
        """
        Initialize payment processor with optional default strategy.
        
        Args:
            payment_strategy: Default payment strategy to use
        """
        self._payment_strategy = payment_strategy
        self.payment_history: List[dict] = []
    
    def set_payment_strategy(self, payment_strategy: PaymentStrategy) -> None:
        """
        Set or change the payment strategy at runtime.
        
        This demonstrates the key benefit of the Strategy Pattern - the ability
        to change algorithms (payment methods) at runtime.
        
        Args:
            payment_strategy: New payment strategy to use
        """
        self._payment_strategy = payment_strategy
        print(f"💰 Payment method set to: {payment_strategy.get_payment_method_name()}")
    
    def process_payment(self, amount: float, payment_info: dict) -> dict:
        """
        Process payment using the current strategy.
        
        Args:
            amount: Payment amount
            payment_info: Payment method specific information
            
        Returns:
            Payment result dictionary
            
        Raises:
            ValueError: If no payment strategy is set or payment info is invalid
        """
        if not self._payment_strategy:
            raise ValueError("No payment strategy set. Please select a payment method.")
        
        # Validate payment information using the strategy
        if not self._payment_strategy.validate_payment_info(payment_info):
            return {
                'success': False,
                'error': 'Invalid payment information',
                'payment_method': self._payment_strategy.get_payment_method_name()
            }
        
        # Process payment using the strategy
        result = self._payment_strategy.process_payment(amount, payment_info)
        
        # Store payment attempt in history
        self.payment_history.append({
            'timestamp': datetime.now(),
            'amount': amount,
            'result': result
        })
        
        return result
    
    def get_available_payment_methods(self) -> List[str]:
        """
        Get list of available payment methods.
        
        Returns:
            List of payment method names
        """
        return ["Credit Card", "Venmo", "PayPal"]
    
    def get_payment_history(self) -> List[dict]:
        """
        Get payment history for this processor.
        
        Returns:
            List of payment attempt records
        """
        return self.payment_history

class OrderStatus(Enum):
    RECEIVED = "received"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"