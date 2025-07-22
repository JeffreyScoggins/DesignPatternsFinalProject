"""
Notification System using Observer Pattern

This package implements the Observer Pattern for notification handling,
allowing different notification types to be managed independently.
"""

from .notification_system import NotificationObserver, NotificationEvent, NotificationChannel
from .customer import CustomerNotifier
from .staff import StaffNotifier
from .promotional import PromotionalSubscriber

__all__ = [
    'NotificationObserver',
    'NotificationEvent',
    'NotificationChannel',
    'CustomerNotifier',
    'StaffNotifier',
    'PromotionalSubscriber'
]
