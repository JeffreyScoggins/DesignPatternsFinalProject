"""
Base Notification System Interfaces and Types
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class NotificationChannel(Enum):
    """Notification delivery channels"""
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"
    IN_APP = "in_app"
    SLACK = "slack"
    WEBHOOK = "webhook"


class NotificationPriority(Enum):
    """Notification priority levels"""
    LOW = "low"
    NORMAL = "normal" 
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class NotificationEvent:
    """Standardized notification event"""
    event_type: str
    data: Dict[str, Any]
    priority: NotificationPriority = NotificationPriority.NORMAL
    channels: Optional[List[NotificationChannel]] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.channels is None:
            self.channels = [NotificationChannel.EMAIL, NotificationChannel.SMS]


@dataclass 
class NotificationResult:
    """Result of notification delivery attempt"""
    success: bool
    channel: NotificationChannel
    recipient: str
    message: str
    error_message: Optional[str] = None
    delivery_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class NotificationTemplate:
    """Template for notification messages"""
    
    def __init__(self, template_id: str, templates: Dict[NotificationChannel, str]):
        self.template_id = template_id
        self.templates = templates
    
    def format_message(self, channel: NotificationChannel, **kwargs) -> str:
        """Format template with provided data"""
        if channel not in self.templates:
            raise ValueError(f"No template found for channel {channel.value}")
        
        template = self.templates[channel]
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing template variable: {e}")


class NotificationObserver(ABC):
    """
    Abstract Observer Interface for Notifications
    
    Enhanced version of the basic Observer that provides:
    - Support for multiple notification channels
    - Priority-based message handling
    - Template-based message formatting
    - Delivery status tracking
    """
    
    def __init__(self, recipient_id: str):
        self.recipient_id = recipient_id
        self.notification_history: List[NotificationResult] = []
        self.preferred_channels: List[NotificationChannel] = [
            NotificationChannel.EMAIL, 
            NotificationChannel.SMS
        ]
    
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> List[NotificationResult]:
        """
        Process notification event and return delivery results
        
        Args:
            event_type: Type of event that triggered the notification
            data: Event data for message formatting
            
        Returns:
            List of NotificationResult objects for each delivery attempt
        """
        pass
    
    @abstractmethod
    def supports_event(self, event_type: str) -> bool:
        """Check if this observer handles the given event type"""
        pass
    
    @abstractmethod
    def get_notification_templates(self) -> Dict[str, NotificationTemplate]:
        """Get notification templates for this observer"""
        pass
    
    def set_preferred_channels(self, channels: List[NotificationChannel]) -> None:
        """Set preferred notification channels"""
        self.preferred_channels = channels
    
    def get_notification_history(self) -> List[NotificationResult]:
        """Get notification delivery history"""
        return self.notification_history.copy()
    
    def _add_to_history(self, result: NotificationResult) -> None:
        """Add notification result to history"""
        self.notification_history.append(result)
    
    def _format_timestamp(self) -> str:
        """Get formatted timestamp for notifications"""
        return datetime.now().strftime("%H:%M:%S")
    
    def _simulate_delivery(self, channel: NotificationChannel, recipient: str, message: str) -> NotificationResult:
        """
        Simulate message delivery (in real app, this would integrate with actual services)
        """
        import random
        
        # Simulate delivery success rates by channel
        success_rates = {
            NotificationChannel.SMS: 0.98,
            NotificationChannel.EMAIL: 0.95,
            NotificationChannel.PUSH: 0.90,
            NotificationChannel.IN_APP: 0.99,
            NotificationChannel.SLACK: 0.97,
            NotificationChannel.WEBHOOK: 0.93
        }
        
        success = random.random() < success_rates.get(channel, 0.95)
        
        if success:
            delivery_id = f"{channel.value}_{random.randint(100000, 999999)}"
            result = NotificationResult(
                success=True,
                channel=channel,
                recipient=recipient,
                message=message,
                delivery_id=delivery_id
            )
        else:
            result = NotificationResult(
                success=False,
                channel=channel,
                recipient=recipient,
                message=message,
                error_message=f"{channel.value} delivery failed"
            )
        
        self._add_to_history(result)
        return result
