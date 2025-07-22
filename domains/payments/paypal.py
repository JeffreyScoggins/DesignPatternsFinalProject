"""
PayPal Payment Strategy Implementation
"""
import random
import re
from typing import Dict, Any

from .base import PaymentStrategy, PaymentResult, PaymentStatus


class PayPalPayment(PaymentStrategy):
    """Concrete Strategy: PayPal Payment"""
    
    def get_payment_method_name(self) -> str:
        return "PayPal"
    
    def get_required_fields(self) -> list[str]:
        return ['paypal_email']
    
    def get_supported_currencies(self) -> list[str]:
        """PayPal supports many currencies"""
        return ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CHF", "SEK", "NOK", "DKK"]
    
    def calculate_fees(self, amount: float) -> float:
        """PayPal processing fee: 2.9% + $0.30 for domestic payments"""
        return (amount * 0.029) + 0.30
    
    def validate_payment_info(self, payment_info: Dict[str, Any]) -> bool:
        """Validate PayPal payment information."""
        try:
            # Check required fields
            for field in self.get_required_fields():
                if field not in payment_info or not payment_info[field]:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            # Validate email format
            email = payment_info['paypal_email']
            if not self._validate_email(email):
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Validation error: {str(e)}")
            return False
    
    def process_payment(self, amount: float, customer_info: Dict[str, Any]) -> PaymentResult:
        """Process PayPal payment."""
        try:
            print(f"💙 Processing PayPal payment of ${amount:.2f}...")
            
            paypal_email = customer_info.get('paypal_email', 'unknown@email.com')
            
            print(f"   PayPal Email: {paypal_email}")
            print(f"   Redirecting to PayPal secure checkout...")
            
            # Simulate payment processing
            success = random.random() > 0.02  # 98% success rate
            
            if success:
                transaction_id = self._generate_transaction_id("PP")
                fees = self.calculate_fees(amount)
                
                print(f"   ✅ PayPal payment successful! Transaction ID: {transaction_id}")
                print(f"   🔒 Payment processed securely through PayPal")
                print(f"   💰 Processing fee: ${fees:.2f}")
                
                return PaymentResult(
                    status=PaymentStatus.SUCCESS,
                    transaction_id=transaction_id,
                    amount=amount,
                    payment_method=self.get_payment_method_name(),
                    additional_data={
                        'paypal_email': paypal_email,
                        'processing_fee': fees,
                        'payment_gateway': 'PayPal Secure Checkout'
                    }
                )
            else:
                print(f"   ❌ PayPal payment failed! Please try again.")
                return PaymentResult(
                    status=PaymentStatus.FAILED,
                    payment_method=self.get_payment_method_name(),
                    error_message='PayPal transaction failed',
                    amount=amount
                )
                
        except Exception as e:
            return PaymentResult(
                status=PaymentStatus.FAILED,
                payment_method=self.get_payment_method_name(),
                error_message=f"Processing error: {str(e)}",
                amount=amount
            )
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            print("❌ Invalid email format")
            return False
        
        return True
