"""
Customer Notification Implementation
"""
from typing import Dict, Any, List
from .notification_system import (
    NotificationObserver, 
    NotificationResult, 
    NotificationTemplate, 
    NotificationChannel
)


class CustomerNotifier(NotificationObserver):
    """Notifies customers about their order status"""
    
    def __init__(self, customer_name: str, phone: str = "", email: str = ""):
        super().__init__(recipient_id=f"customer_{customer_name}")
        self.customer_name = customer_name
        self.phone = phone
        self.email = email
        
        # Set preferred channels based on contact info
        preferred = []
        if email:
            preferred.append(NotificationChannel.EMAIL)
        if phone:
            preferred.append(NotificationChannel.SMS)
        if preferred:
            self.set_preferred_channels(preferred)
    
    def supports_event(self, event_type: str) -> bool:
        """Customer notifications support order and payment events"""
        return event_type in [
            "order_received",
            "order_preparing", 
            "order_ready",
            "order_delivered",
            "payment_successful",
            "payment_failed"
        ]
    
    def get_notification_templates(self) -> Dict[str, NotificationTemplate]:
        """Get customer notification templates"""
        return {
            "order_received": NotificationTemplate(
                "order_received",
                {
                    NotificationChannel.SMS: "Your order #{order_id} has been received! Total: ${total:.2f}",
                    NotificationChannel.EMAIL: "Hi {customer_name}, your order #{order_id} has been received! Total: ${total:.2f}. We'll notify you when it's ready.",
                    NotificationChannel.PUSH: "Order #{order_id} received - ${total:.2f}"
                }
            ),
            "order_preparing": NotificationTemplate(
                "order_preparing",
                {
                    NotificationChannel.SMS: "Your order #{order_id} is now being prepared. ETA: {eta} minutes",
                    NotificationChannel.EMAIL: "Good news {customer_name}! Your order #{order_id} is now being prepared. Estimated time: {eta} minutes.",
                    NotificationChannel.PUSH: "Order #{order_id} is being prepared - ETA {eta} min"
                }
            ),
            "order_ready": NotificationTemplate(
                "order_ready",
                {
                    NotificationChannel.SMS: "Your order #{order_id} is ready for pickup/delivery!",
                    NotificationChannel.EMAIL: "Great news {customer_name}! Your order #{order_id} is ready for pickup/delivery!",
                    NotificationChannel.PUSH: "Order #{order_id} is ready!"
                }
            ),
            "order_delivered": NotificationTemplate(
                "order_delivered",
                {
                    NotificationChannel.SMS: "Your order #{order_id} has been delivered. Thank you!",
                    NotificationChannel.EMAIL: "Thank you {customer_name}! Your order #{order_id} has been delivered. We hope you enjoy your meal!",
                    NotificationChannel.PUSH: "Order #{order_id} delivered. Thank you!"
                }
            ),
            "payment_successful": NotificationTemplate(
                "payment_successful",
                {
                    NotificationChannel.SMS: "Payment confirmed! ${amount:.2f} via {payment_method} (ID: {transaction_id})",
                    NotificationChannel.EMAIL: "Hi {customer_name}, your payment of ${amount:.2f} via {payment_method} has been confirmed. Transaction ID: {transaction_id}",
                    NotificationChannel.PUSH: "Payment confirmed - ${amount:.2f}"
                }
            ),
            "payment_failed": NotificationTemplate(
                "payment_failed",
                {
                    NotificationChannel.SMS: "Payment failed for order #{order_id}. Please try a different payment method.",
                    NotificationChannel.EMAIL: "Hi {customer_name}, payment failed for order #{order_id}. Please try a different payment method or contact support.",
                    NotificationChannel.PUSH: "Payment failed - please retry"
                }
            )
        }
    
    def update(self, event_type: str, data: Dict[str, Any]) -> List[NotificationResult]:
        """Process customer notification"""
        if not self.supports_event(event_type):
            return []
        
        results = []
        templates = self.get_notification_templates()
        
        if event_type not in templates:
            return []
        
        template = templates[event_type]
        timestamp = self._format_timestamp()
        
        # Add customer name to data for template formatting
        data_with_customer = {**data, 'customer_name': self.customer_name}
        
        # Send notification via preferred channels
        for channel in self.preferred_channels:
            try:
                message = template.format_message(channel, **data_with_customer)
                
                # Display the notification (in real app, this would use actual services)
                recipient = self.email if channel == NotificationChannel.EMAIL else self.phone
                print(f"[{timestamp}] {channel.value.upper()} to {self.customer_name}: {message}")
                
                # Simulate delivery
                result = self._simulate_delivery(channel, recipient, message)
                results.append(result)
                
            except Exception as e:
                # Handle template formatting errors
                error_result = NotificationResult(
                    success=False,
                    channel=channel,
                    recipient=self.customer_name,
                    message="",
                    error_message=f"Template formatting error: {str(e)}"
                )
                results.append(error_result)
                self._add_to_history(error_result)
        
        return results
    
    def get_contact_info(self) -> Dict[str, str]:
        """Get customer contact information"""
        return {
            'name': self.customer_name,
            'phone': self.phone,
            'email': self.email
        }
