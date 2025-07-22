"""
Payment Processor - Context class for Strategy Pattern
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base import PaymentStrategy, PaymentResult, PaymentStatus, PaymentError


class PaymentProcessor:
    """
    Context class for Strategy Pattern
    
    This class manages payment processing and maintains the strategy pattern
    by delegating payment processing to the selected payment strategy.
    """
    
    def __init__(self, payment_strategy: Optional[PaymentStrategy] = None):
        """Initialize payment processor with optional default strategy."""
        self._payment_strategy = payment_strategy
        self.payment_history: List[Dict[str, Any]] = []
    
    def set_payment_strategy(self, payment_strategy: PaymentStrategy) -> None:
        """
        Set or change the payment strategy at runtime.
        
        This is the key method that enables the Strategy pattern's flexibility -
        the payment method can be changed without modifying the processor.
        """
        self._payment_strategy = payment_strategy
        print(f"💰 Payment method set to: {payment_strategy.get_payment_method_name()}")
    
    def get_current_strategy(self) -> Optional[PaymentStrategy]:
        """Get the currently set payment strategy."""
        return self._payment_strategy
    
    def process_payment(self, amount: float, payment_info: Dict[str, Any]) -> PaymentResult:
        """
        Process payment using the current strategy.
        
        Args:
            amount: Payment amount
            payment_info: Payment method specific information
            
        Returns:
            PaymentResult object with transaction details
            
        Raises:
            PaymentError: If no strategy is set or validation fails
        """
        if not self._payment_strategy:
            raise PaymentError(
                "No payment strategy set. Please select a payment method.",
                error_code="NO_STRATEGY"
            )
        
        try:
            # Validate payment information
            if not self._payment_strategy.validate_payment_info(payment_info):
                result = PaymentResult(
                    status=PaymentStatus.FAILED,
                    payment_method=self._payment_strategy.get_payment_method_name(),
                    error_message='Invalid payment information',
                    amount=amount
                )
            else:
                # Process the payment
                result = self._payment_strategy.process_payment(amount, payment_info)
            
            # Store in payment history
            self._add_to_history(amount, result, payment_info)
            
            return result
            
        except Exception as e:
            error_result = PaymentResult(
                status=PaymentStatus.FAILED,
                payment_method=self._payment_strategy.get_payment_method_name() if self._payment_strategy else "Unknown",
                error_message=f"Unexpected error: {str(e)}",
                amount=amount
            )
            self._add_to_history(amount, error_result, payment_info)
            return error_result
    
    def get_available_payment_methods(self) -> List[str]:
        """Get list of available payment methods."""
        # In a real application, this might be dynamically loaded
        return ["Credit Card", "Venmo", "PayPal"]
    
    def get_payment_history(self) -> List[Dict[str, Any]]:
        """Get payment history for this processor."""
        return self.payment_history.copy()  # Return a copy to prevent modification
    
    def get_successful_payments(self) -> List[Dict[str, Any]]:
        """Get only successful payments from history."""
        return [
            payment for payment in self.payment_history 
            if payment['result']['success']
        ]
    
    def get_failed_payments(self) -> List[Dict[str, Any]]:
        """Get only failed payments from history."""
        return [
            payment for payment in self.payment_history 
            if not payment['result']['success']
        ]
    
    def get_total_processed(self) -> float:
        """Get total amount of successful payments processed."""
        return sum(
            payment['amount'] for payment in self.payment_history
            if payment['result']['success']
        )
    
    def calculate_processing_fees(self, amount: float) -> float:
        """Calculate processing fees for current payment method."""
        if not self._payment_strategy:
            return 0.0
        return self._payment_strategy.calculate_fees(amount)
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for current payment method."""
        if not self._payment_strategy:
            return []
        return self._payment_strategy.get_required_fields()
    
    def supports_currency(self, currency: str) -> bool:
        """Check if current payment method supports the given currency."""
        if not self._payment_strategy:
            return False
        return currency in self._payment_strategy.get_supported_currencies()
    
    def _add_to_history(self, amount: float, result: PaymentResult, payment_info: Dict[str, Any]) -> None:
        """Add payment attempt to history."""
        # Create a sanitized copy of payment_info (remove sensitive data)
        safe_payment_info = self._sanitize_payment_info(payment_info)
        
        history_entry = {
            'timestamp': datetime.now(),
            'amount': amount,
            'result': result.to_dict(),
            'payment_info': safe_payment_info
        }
        
        self.payment_history.append(history_entry)
    
    def _sanitize_payment_info(self, payment_info: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive information from payment info for logging."""
        sensitive_fields = ['card_number', 'cvv', 'password', 'pin']
        sanitized = {}
        
        for key, value in payment_info.items():
            if key.lower() in sensitive_fields:
                sanitized[key] = '***REDACTED***'
            elif key == 'card_number' and isinstance(value, str):
                # For card numbers, show only last 4 digits
                clean_number = value.replace('-', '').replace(' ', '')
                if len(clean_number) >= 4:
                    sanitized[key] = f"****-****-****-{clean_number[-4:]}"
                else:
                    sanitized[key] = '***REDACTED***'
            else:
                sanitized[key] = value
        
        return sanitized
