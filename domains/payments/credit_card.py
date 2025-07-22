"""
Credit Card Payment Strategy Implementation
"""
import random
import re
from typing import Dict, Any

from .base import PaymentStrategy, PaymentResult, PaymentStatus, PaymentError


class CreditCardPayment(PaymentStrategy):
    """Concrete Strategy: Credit Card Payment"""
    
    def get_payment_method_name(self) -> str:
        return "Credit Card"
    
    def get_required_fields(self) -> list[str]:
        return ['card_number', 'expiry', 'cvv', 'cardholder_name']
    
    def calculate_fees(self, amount: float) -> float:
        """Credit card processing fee: 2.9% + $0.30"""
        return (amount * 0.029) + 0.30
    
    def validate_payment_info(self, payment_info: Dict[str, Any]) -> bool:
        """Validate credit card information."""
        try:
            # Check required fields
            for field in self.get_required_fields():
                if field not in payment_info or not payment_info[field]:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            # Validate card number
            card_number = payment_info['card_number'].replace('-', '').replace(' ', '')
            if not self._validate_card_number(card_number):
                return False
            
            # Validate expiry
            if not self._validate_expiry(payment_info['expiry']):
                return False
            
            # Validate CVV
            if not self._validate_cvv(payment_info['cvv']):
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Validation error: {str(e)}")
            return False
    
    def process_payment(self, amount: float, customer_info: Dict[str, Any]) -> PaymentResult:
        """Process credit card payment."""
        try:
            print(f"💳 Processing credit card payment of ${amount:.2f}...")
            
            card_number = customer_info.get('card_number', '****-****-****-****')
            masked_card = self._mask_card_number(card_number)
            
            print(f"   Card: {masked_card}")
            print(f"   Cardholder: {customer_info.get('cardholder_name', 'N/A')}")
            print(f"   Processing through secure payment gateway...")
            
            # Simulate payment processing
            success = random.random() > 0.05  # 95% success rate
            
            if success:
                transaction_id = self._generate_transaction_id("CC")
                fees = self.calculate_fees(amount)
                
                print(f"   ✅ Payment successful! Transaction ID: {transaction_id}")
                print(f"   💰 Processing fee: ${fees:.2f}")
                
                return PaymentResult(
                    status=PaymentStatus.SUCCESS,
                    transaction_id=transaction_id,
                    amount=amount,
                    payment_method=self.get_payment_method_name(),
                    additional_data={
                        'masked_card': masked_card,
                        'processing_fee': fees,
                        'cardholder_name': customer_info.get('cardholder_name')
                    }
                )
            else:
                print(f"   ❌ Payment failed! Please check your card information.")
                return PaymentResult(
                    status=PaymentStatus.FAILED,
                    payment_method=self.get_payment_method_name(),
                    error_message='Card declined',
                    amount=amount
                )
                
        except Exception as e:
            return PaymentResult(
                status=PaymentStatus.FAILED,
                payment_method=self.get_payment_method_name(),
                error_message=f"Processing error: {str(e)}",
                amount=amount
            )
    
    def _validate_card_number(self, card_number: str) -> bool:
        """Validate card number using Luhn algorithm"""
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            print("❌ Invalid card number format")
            return False
        
        # Basic Luhn algorithm check
        total = 0
        reverse_digits = card_number[::-1]
        
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        
        if total % 10 != 0:
            print("❌ Invalid card number (failed Luhn check)")
            return False
        
        return True
    
    def _validate_expiry(self, expiry: str) -> bool:
        """Validate expiry date format and ensure it's not expired"""
        if not re.match(r'^\d{2}/\d{2}$', expiry):
            print("❌ Invalid expiry format (use MM/YY)")
            return False
        
        # Additional expiry validation could be added here
        return True
    
    def _validate_cvv(self, cvv: str) -> bool:
        """Validate CVV format"""
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            print("❌ Invalid CVV format")
            return False
        return True
    
    def _mask_card_number(self, card_number: str) -> str:
        """Mask card number for display"""
        clean_number = card_number.replace('-', '').replace(' ', '')
        if len(clean_number) >= 4:
            return f"****-****-****-{clean_number[-4:]}"
        return "****-****-****-****"
