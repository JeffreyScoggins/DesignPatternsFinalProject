"""
Staff Notification Implementation
"""
from typing import Dict, Any, List
from .notification_system import (
    NotificationObserver, 
    NotificationResult, 
    NotificationTemplate, 
    NotificationChannel
)


class StaffNotifier(NotificationObserver):
    """Notifies restaurant staff about order updates"""
    
    def __init__(self, staff_name: str, role: str):
        super().__init__(recipient_id=f"staff_{staff_name}")
        self.staff_name = staff_name
        self.role = role.lower()
        
        # Staff typically use different channels
        self.set_preferred_channels([
            NotificationChannel.SLACK,
            NotificationChannel.IN_APP,
            NotificationChannel.PUSH
        ])
    
    def supports_event(self, event_type: str) -> bool:
        """Check if this staff member should receive notifications for this event type"""
        role_events = {
            "kitchen": ["order_received", "order_preparing"],
            "server": ["order_preparing", "order_ready"],
            "manager": ["order_received", "order_ready", "payment_successful", "payment_failed"],
            "cashier": ["payment_successful", "payment_failed"]
        }
        
        return event_type in role_events.get(self.role, [])
    
    def get_notification_templates(self) -> Dict[str, NotificationTemplate]:
        """Get staff notification templates based on role"""
        return {
            "order_received": NotificationTemplate(
                "order_received",
                {
                    NotificationChannel.SLACK: "🍽️ New order #{order_id} received - {item_count} items",
                    NotificationChannel.IN_APP: "NEW ORDER: #{order_id} ({item_count} items)",
                    NotificationChannel.PUSH: "New order #{order_id} - {item_count} items"
                }
            ),
            "order_preparing": NotificationTemplate(
                "order_preparing", 
                {
                    NotificationChannel.SLACK: "👨‍🍳 Order #{order_id} in preparation",
                    NotificationChannel.IN_APP: "PREPARING: Order #{order_id}",
                    NotificationChannel.PUSH: "Order #{order_id} in preparation"
                }
            ),
            "order_ready": NotificationTemplate(
                "order_ready",
                {
                    NotificationChannel.SLACK: "✅ Order #{order_id} ready for service!",
                    NotificationChannel.IN_APP: "READY: Order #{order_id} - ready for service!",
                    NotificationChannel.PUSH: "Order #{order_id} ready for service!"
                }
            ),
            "payment_successful": NotificationTemplate(
                "payment_successful",
                {
                    NotificationChannel.SLACK: "💰 Payment received! Order #{order_id} - ${amount:.2f} via {payment_method}",
                    NotificationChannel.IN_APP: "PAYMENT: Order #{order_id} - ${amount:.2f} via {payment_method}",
                    NotificationChannel.PUSH: "Payment received - ${amount:.2f}"
                }
            ),
            "payment_failed": NotificationTemplate(
                "payment_failed",
                {
                    NotificationChannel.SLACK: "❌ Payment FAILED for order #{order_id} - Requires attention!",
                    NotificationChannel.IN_APP: "PAYMENT FAILED: Order #{order_id} - action required",
                    NotificationChannel.PUSH: "Payment failed - order #{order_id}"
                }
            )
        }
    
    def update(self, event_type: str, data: Dict[str, Any]) -> List[NotificationResult]:
        """Process staff notification"""
        if not self.supports_event(event_type):
            return []
        
        results = []
        templates = self.get_notification_templates()
        
        if event_type not in templates:
            return []
        
        template = templates[event_type]
        timestamp = self._format_timestamp()
        
        # Add staff info and item count to data
        data_with_staff = {
            **data, 
            'staff_name': self.staff_name,
            'role': self.role,
            'item_count': len(data.get('items', []))
        }
        
        # Send notification via preferred channels
        for channel in self.preferred_channels:
            try:
                message = template.format_message(channel, **data_with_staff)
                
                # Display the notification (in real app, this would use actual services)
                print(f"[{timestamp}] STAFF ALERT ({self.staff_name} - {self.role}): {message}")
                
                # Simulate delivery
                result = self._simulate_delivery(channel, self.staff_name, message)
                results.append(result)
                
            except Exception as e:
                # Handle template formatting errors
                error_result = NotificationResult(
                    success=False,
                    channel=channel,
                    recipient=self.staff_name,
                    message="",
                    error_message=f"Template formatting error: {str(e)}"
                )
                results.append(error_result)
                self._add_to_history(error_result)
        
        return results
    
    def get_staff_info(self) -> Dict[str, str]:
        """Get staff member information"""
        return {
            'name': self.staff_name,
            'role': self.role
        }
    
    def get_supported_events(self) -> List[str]:
        """Get list of events this staff member receives notifications for"""
        role_events = {
            "kitchen": ["order_received", "order_preparing"],
            "server": ["order_preparing", "order_ready"],
            "manager": ["order_received", "order_ready", "payment_successful", "payment_failed"],
            "cashier": ["payment_successful", "payment_failed"]
        }
        return role_events.get(self.role, [])
