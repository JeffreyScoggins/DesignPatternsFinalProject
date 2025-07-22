"""
Promotional Notification Implementation
"""
from typing import Dict, Any, List, Optional
from .notification_system import (
    NotificationObserver, 
    NotificationResult, 
    NotificationTemplate, 
    NotificationChannel
)


class PromotionalSubscriber(NotificationObserver):
    """Handles promotional emails and special deals"""
    
    def __init__(self, customer_name: str, email: str, preferences: Optional[List[str]] = None):
        super().__init__(recipient_id=f"promo_{customer_name}")
        self.customer_name = customer_name
        self.email = email
        self.preferences = preferences if preferences is not None else []
        
        # Promotional notifications typically use email and push
        self.set_preferred_channels([
            NotificationChannel.EMAIL,
            NotificationChannel.PUSH
        ])
    
    def supports_event(self, event_type: str) -> bool:
        """Promotional subscriber handles marketing events"""
        return event_type in [
            "promotion",
            "loyalty_reward",
            "birthday_offer",
            "seasonal_promotion",
            "new_menu_item",
            "special_event"
        ]
    
    def get_notification_templates(self) -> Dict[str, NotificationTemplate]:
        """Get promotional notification templates"""
        return {
            "promotion": NotificationTemplate(
                "promotion",
                {
                    NotificationChannel.EMAIL: "🎉 Hi {customer_name}! {message} Use code: {promo_code}",
                    NotificationChannel.PUSH: "🎉 {message}"
                }
            ),
            "loyalty_reward": NotificationTemplate(
                "loyalty_reward",
                {
                    NotificationChannel.EMAIL: "🌟 Congratulations {customer_name}! {message}",
                    NotificationChannel.PUSH: "🌟 Loyalty reward: {message}"
                }
            ),
            "birthday_offer": NotificationTemplate(
                "birthday_offer",
                {
                    NotificationChannel.EMAIL: "🎂 Happy Birthday {customer_name}! {message}",
                    NotificationChannel.PUSH: "🎂 Birthday special: {message}"
                }
            ),
            "seasonal_promotion": NotificationTemplate(
                "seasonal_promotion",
                {
                    NotificationChannel.EMAIL: "🍂 Seasonal Special for {customer_name}! {message}",
                    NotificationChannel.PUSH: "🍂 Seasonal: {message}"
                }
            ),
            "new_menu_item": NotificationTemplate(
                "new_menu_item",
                {
                    NotificationChannel.EMAIL: "🍽️ New on the menu, {customer_name}! {message}",
                    NotificationChannel.PUSH: "🍽️ New: {message}"
                }
            ),
            "special_event": NotificationTemplate(
                "special_event",
                {
                    NotificationChannel.EMAIL: "🎪 Special Event for {customer_name}! {message}",
                    NotificationChannel.PUSH: "🎪 Event: {message}"
                }
            )
        }
    
    def update(self, event_type: str, data: Dict[str, Any]) -> List[NotificationResult]:
        """Process promotional notification"""
        if not self.supports_event(event_type):
            return []
        
        # Check if customer has preferences and if this promotion matches
        if self.preferences and event_type == "promotion":
            category = data.get('category', '')
            if category and category not in self.preferences:
                return []  # Skip if not in customer's preferences
        
        results = []
        templates = self.get_notification_templates()
        
        if event_type not in templates:
            return []
        
        template = templates[event_type]
        timestamp = self._format_timestamp()
        
        # Add customer info to data
        data_with_customer = {
            **data,
            'customer_name': self.customer_name
        }
        
        # Send notification via preferred channels
        for channel in self.preferred_channels:
            try:
                message = template.format_message(channel, **data_with_customer)
                
                # Display the notification
                channel_prefix = "PROMO EMAIL" if channel == NotificationChannel.EMAIL else "PROMO PUSH"
                print(f"[{timestamp}] {channel_prefix} to {self.customer_name}: {message}")
                
                # Simulate delivery
                result = self._simulate_delivery(channel, self.email, message)
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
    
    def add_preference(self, preference: str) -> None:
        """Add a promotional preference"""
        if preference not in self.preferences:
            self.preferences.append(preference)
    
    def remove_preference(self, preference: str) -> None:
        """Remove a promotional preference"""
        if preference in self.preferences:
            self.preferences.remove(preference)
    
    def get_preferences(self) -> List[str]:
        """Get customer's promotional preferences"""
        return self.preferences.copy()
    
    def get_subscriber_info(self) -> Dict[str, Any]:
        """Get subscriber information"""
        return {
            'name': self.customer_name,
            'email': self.email,
            'preferences': self.preferences
        }
