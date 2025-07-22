"""
Base Payment Strategy Interface and Common Types
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PaymentStatus(Enum):
    """Payment status enumeration"""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    CANCELLED = "cancelled"


@dataclass
class PaymentResult:
    """Standardized payment result"""
    status: PaymentStatus
    transaction_id: Optional[str] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    error_message: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    @property
    def success(self) -> bool:
        """Check if payment was successful"""
        return self.status == PaymentStatus.SUCCESS
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        result = {
            'success': self.success,
            'status': self.status.value,
            'timestamp': self.timestamp.isoformat() if self.timestamp else datetime.now().isoformat()
        }
        
        if self.transaction_id:
            result['transaction_id'] = self.transaction_id
        if self.amount is not None:
            result['amount'] = self.amount
        if self.payment_method:
            result['payment_method'] = self.payment_method
        if self.error_message:
            result['error_message'] = self.error_message
        if self.additional_data:
            result.update(self.additional_data)
            
        return result


class PaymentError(Exception):
    """Custom exception for payment-related errors"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class PaymentStrategy(ABC):
    """
    Abstract Strategy Interface (Strategy Pattern)
    
    This defines the interface that all concrete payment strategies must implement.
    The Strategy pattern allows the payment method to be selected and changed at runtime
    without modifying the client code.
    """
    
    @abstractmethod
    def process_payment(self, amount: float, customer_info: Dict[str, Any]) -> PaymentResult:
        """
        Process payment using the specific payment method.
        
        Args:
            amount: Payment amount
            customer_info: Customer and payment information
            
        Returns:
            PaymentResult object with transaction details
        """
        pass
    
    @abstractmethod
    def validate_payment_info(self, payment_info: Dict[str, Any]) -> bool:
        """
        Validate payment information for this payment method.
        
        Args:
            payment_info: Payment method specific information
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_payment_method_name(self) -> str:
        """Get the display name of this payment method."""
        pass
    
    @abstractmethod
    def get_required_fields(self) -> list[str]:
        """Get list of required fields for this payment method."""
        pass
    
    def get_supported_currencies(self) -> list[str]:
        """Get list of supported currencies. Override if payment method has restrictions."""
        return ["USD", "EUR", "GBP", "CAD"]
    
    def calculate_fees(self, amount: float) -> float:
        """Calculate processing fees. Override for payment-specific fees."""
        return 0.0
    
    def _generate_transaction_id(self, prefix: str) -> str:
        """Generate a unique transaction ID"""
        import random
        return f"{prefix}_{random.randint(100000, 999999)}"
