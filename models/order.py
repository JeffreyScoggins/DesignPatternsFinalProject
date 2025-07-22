"""
Order model with integrated Observer and Strategy Patterns
"""
from typing import List, Optional
from datetime import datetime

from config.enums import OrderStatus
from core.base_classes import Subject
from domains.menu import MenuItemBase
from domains.notifications import CustomerNotifier, StaffNotifier
from domains.payments import (
    PaymentProcessor, 
    CreditCardPayment, 
    VenmoPayment, 
    PayPalPayment,
    PaymentResult
)


class Order(Subject):
    """Order class with Observer Pattern for notifications and Strategy Pattern for payments"""
    _order_counter = 1
    
    def __init__(self, customer_name: str, customer_phone: str = "", customer_email: str = ""):
        super().__init__()
        self.order_id = Order._order_counter
        Order._order_counter += 1
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_email = customer_email
        self.items: List[MenuItemBase] = []
        self.total_price = 0.0
        self.status = OrderStatus.RECEIVED
        self.created_at = datetime.now()
        
        # Strategy Pattern Integration: Payment Processing
        self.payment_processor = PaymentProcessor()
        self.payment_info: Optional[dict] = None
        self.payment_result: Optional[PaymentResult] = None
        
        # Auto-attach customer notifier if contact info provided
        if customer_phone or customer_email:
            customer_notifier = CustomerNotifier(customer_name, customer_phone, customer_email)
            self.attach(customer_notifier)
    
    def set_payment_method(self, payment_method: str) -> bool:
        """Set payment method using Strategy Pattern"""
        payment_strategies = {
            'credit_card': CreditCardPayment(),
            'venmo': VenmoPayment(),
            'paypal': PayPalPayment()
        }
        
        if payment_method.lower() in payment_strategies:
            self.payment_processor.set_payment_strategy(payment_strategies[payment_method.lower()])
            return True
        else:
            print(f"❌ Invalid payment method: {payment_method}")
            return False
    
    def add_payment_info(self, payment_info: dict) -> None:
        """Add payment information for the order"""
        self.payment_info = payment_info
        print(f"💳 Payment information added for order #{self.order_id}")
    
    def add_item(self, item: MenuItemBase) -> None:
        """Add an item to the order"""
        self.items.append(item)
        self.total_price += item.price
        print(f"Added {item.name} to order #{self.order_id}")
    
    def remove_item(self, item_name: str) -> bool:
        """Remove an item from the order"""
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                self.total_price -= item.price
                print(f"Removed {item_name} from order #{self.order_id}")
                return True
        print(f"Item {item_name} not found in order #{self.order_id}")
        return False
    
    def calculate_total(self) -> float:
        """Calculate and return the total price"""
        self.total_price = sum(item.price for item in self.items)
        return self.total_price
    
    def get_estimated_time(self) -> int:
        """Calculate estimated preparation time"""
        if not self.items:
            return 0
        return max(item.get_preparation_time() for item in self.items)
    
    def process_payment(self) -> bool:
        """Process payment using the configured strategy"""
        if not self.payment_info:
            print(f"❌ No payment information provided for order #{self.order_id}")
            return False
        
        if not hasattr(self.payment_processor, '_payment_strategy') or not self.payment_processor._payment_strategy:
            print(f"❌ No payment method selected for order #{self.order_id}")
            return False
        
        print(f"\n💰 Processing payment for order #{self.order_id}...")
        print(f"   Customer: {self.customer_name}")
        print(f"   Total Amount: ${self.total_price:.2f}")
        
        # Process payment using Strategy Pattern
        result = self.payment_processor.process_payment(self.total_price, self.payment_info)
        self.payment_result = result
        
        if result.success:
            print(f"🎉 Payment successful for order #{self.order_id}!")
            # Notify observers about successful payment
            self.notify("payment_successful", {
                'order_id': self.order_id,
                'amount': self.total_price,
                'payment_method': result.payment_method,
                'transaction_id': result.transaction_id
            })
            return True
        else:
            print(f"❌ Payment failed for order #{self.order_id}: {result.error_message or 'Unknown error'}")
            # Notify observers about failed payment
            self.notify("payment_failed", {
                'order_id': self.order_id,
                'amount': self.total_price,
                'error': result.error_message or 'Unknown error'
            })
            return False
    
    def update_status(self, new_status: OrderStatus) -> None:
        """Update order status and notify observers"""
        old_status = self.status
        self.status = new_status
        
        # Prepare notification data
        notification_data = {
            'order_id': self.order_id,
            'old_status': old_status.value,
            'new_status': new_status.value,
            'customer_name': self.customer_name,
            'total': self.total_price,
            'items': [item.name for item in self.items],
            'eta': self.get_estimated_time()
        }
        
        # Map status to event type for notifications
        event_mapping = {
            OrderStatus.RECEIVED: "order_received",
            OrderStatus.PREPARING: "order_preparing", 
            OrderStatus.READY: "order_ready",
            OrderStatus.DELIVERED: "order_delivered"
        }
        
        event_type = event_mapping.get(new_status)
        if event_type:
            self.notify(event_type, notification_data)
    
    def display_order(self) -> None:
        """Display order details including payment information"""
        print(f"\nOrder #{self.order_id} for {self.customer_name}:")
        print(f"Status: {self.status.value.title()}")
        print("-" * 50)
        
        for item in self.items:
            print(f"  {item.name} - ${item.price:.2f}")
        
        print("-" * 50)
        print(f"Total: ${self.total_price:.2f}")
        print(f"Estimated preparation time: {self.get_estimated_time()} minutes")
        print("-" * 50)
        
        # Display payment information if available
        if self.payment_result:
            print("💳 PAYMENT INFORMATION:")
            if self.payment_result.success:
                print(f"   ✅ Status: PAID")
                print(f"   💰 Method: {self.payment_result.payment_method}")
                print(f"   🔢 Transaction ID: {self.payment_result.transaction_id}")
                
                # Add payment method specific details from additional_data
                if self.payment_result.additional_data:
                    additional = self.payment_result.additional_data
                    if 'masked_card' in additional:
                        print(f"   💳 Card: {additional['masked_card']}")
                    elif 'venmo_username' in additional:
                        print(f"   📱 Venmo: {additional['venmo_username']}")
                    elif 'paypal_email' in additional:
                        print(f"   💙 PayPal: {additional['paypal_email']}")
            else:
                print(f"   ❌ Status: PAYMENT FAILED")
                print(f"   ❗ Error: {self.payment_result.error_message or 'Unknown error'}")
        elif self.payment_info:
            print("💳 PAYMENT INFORMATION:")
            print(f"   ⏳ Status: PAYMENT PENDING")
            if hasattr(self.payment_processor, '_payment_strategy') and self.payment_processor._payment_strategy:
                print(f"   📋 Method: {self.payment_processor._payment_strategy.get_payment_method_name()}")
        else:
            print("💳 PAYMENT INFORMATION:")
            print(f"   ⚠️  Status: NO PAYMENT METHOD SET")
    
    def __str__(self) -> str:
        """String representation of the order"""
        items_str = ", ".join([item.name for item in self.items])
        return f"Order #{self.order_id}: {items_str} (${self.total_price:.2f}) - {self.status.value}"
