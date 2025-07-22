"""
Payment Processing System using Strategy Pattern

This package implements the Strategy Pattern for payment processing,
allowing different payment methods to be used interchangeably.
"""

from .base import PaymentStrategy, PaymentResult, PaymentError
from .processor import PaymentProcessor
from .credit_card import CreditCardPayment
from .venmo import VenmoPayment
from .paypal import PayPalPayment

__all__ = [
    'PaymentStrategy',
    'PaymentResult', 
    'PaymentError',
    'PaymentProcessor',
    'CreditCardPayment',
    'VenmoPayment',
    'PayPalPayment'
]
