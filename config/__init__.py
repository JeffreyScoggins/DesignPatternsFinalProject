"""
Configuration module.
Contains application configuration and constants.
"""

from .enums import OrderStatus, FoodCategory
from .settings import (
    APP_NAME, APP_VERSION, DEFAULT_RESTAURANT_NAME,
    DEFAULT_PREPARATION_TIME, PAYMENT_SUCCESS_RATES,
    MAX_ITEMS_PER_ORDER, MIN_ORDER_AMOUNT
)

__all__ = [
    # Enums
    'OrderStatus',
    'FoodCategory',
    
    # Settings
    'APP_NAME',
    'APP_VERSION', 
    'DEFAULT_RESTAURANT_NAME',
    'DEFAULT_PREPARATION_TIME',
    'PAYMENT_SUCCESS_RATES',
    'MAX_ITEMS_PER_ORDER',
    'MIN_ORDER_AMOUNT'
]
