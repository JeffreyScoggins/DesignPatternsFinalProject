from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

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