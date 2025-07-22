"""
Configuration constants for the restaurant management system
"""

# Application Configuration
APP_NAME = "BigTown Bistro Restaurant Management System"
APP_VERSION = "1.0.0"

# Restaurant Configuration
DEFAULT_RESTAURANT_NAME = "BigTown Bistro"
DEFAULT_PREPARATION_TIME = 25  # minutes

# Payment Configuration
PAYMENT_SUCCESS_RATES = {
    'credit_card': 0.95,  # 95% success rate
    'venmo': 0.97,        # 97% success rate
    'paypal': 0.98        # 98% success rate
}

# Order Configuration
MAX_ITEMS_PER_ORDER = 20
MIN_ORDER_AMOUNT = 5.00

# Notification Configuration
NOTIFICATION_ENABLED = True
SMS_ENABLED = True
EMAIL_ENABLED = True

# Display Configuration
MENU_DISPLAY_WIDTH = 50
ORDER_DISPLAY_WIDTH = 50
SEPARATOR_CHAR = "="
