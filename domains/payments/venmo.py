"""
Venmo Payment Strategy Implementation
"""
import random
import re
from typing import Dict, Any

from .base import PaymentStrategy, PaymentResult, PaymentStatus


class VenmoPayment(PaymentStrategy):
    """Concrete Strategy: Venmo Payment"""
    
    def get_payment_method_name(self) -> str:
        return "Venmo"
    
    def get_required_fields(self) -> list[str]:
        return ['venmo_username', 'phone']
    
    def get_supported_currencies(self) -> list[str]:
        """Venmo only supports USD"""
        return ["USD"]
    
    def calculate_fees(self, amount: float) -> float:
        """Venmo typically has no fees for standard transfers"""
        return 0.0
    
    def validate_payment_info(self, payment_info: Dict[str, Any]) -> bool:
        """Validate Venmo payment information."""
        try:
            # Check required fields
            for field in self.get_required_fields():
                if field not in payment_info or not payment_info[field]:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            # Validate username format
            username = payment_info['venmo_username']
            if not self._validate_username(username):
                return False
            
            # Validate phone format (basic check)
            phone = payment_info['phone']
            if not self._validate_phone(phone):
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Validation error: {str(e)}")
            return False
    
    def process_payment(self, amount: float, customer_info: Dict[str, Any]) -> PaymentResult:
        """Process Venmo payment."""
        try:
            print(f"📱 Processing Venmo payment of ${amount:.2f}...")
            
            venmo_username = customer_info.get('venmo_username', '@unknown')
            phone = customer_info.get('phone', 'N/A')
            
            print(f"   Venmo: {venmo_username}")
            print(f"   Phone: {phone}")
            print(f"   Sending payment request through Venmo API...")
            
            # Simulate payment processing
            success = random.random() > 0.03  # 97% success rate
            
            if success:
                transaction_id = self._generate_transaction_id("VEN")
                
                print(f"   ✅ Payment successful! Venmo Transaction ID: {transaction_id}")
                print(f"   💬 Payment note: 'Order from BigTown Bistro 🍽️'")
                
                return PaymentResult(
                    status=PaymentStatus.SUCCESS,
                    transaction_id=transaction_id,
                    amount=amount,
                    payment_method=self.get_payment_method_name(),
                    additional_data={
                        'venmo_username': venmo_username,
                        'phone': phone,
                        'payment_note': 'Order from BigTown Bistro 🍽️'
                    }
                )
            else:
                print(f"   ❌ Venmo payment failed! Please check your account.")
                return PaymentResult(
                    status=PaymentStatus.FAILED,
                    payment_method=self.get_payment_method_name(),
                    error_message='Venmo transaction failed',
                    amount=amount
                )
                
        except Exception as e:
            return PaymentResult(
                status=PaymentStatus.FAILED,
                payment_method=self.get_payment_method_name(),
                error_message=f"Processing error: {str(e)}",
                amount=amount
            )
    
    def _validate_username(self, username: str) -> bool:
        """Validate Venmo username format"""
        if not username.startswith('@'):
            print("❌ Invalid Venmo username format (should start with @)")
            return False
        
        if len(username) < 2:
            print("❌ Venmo username too short")
            return False
        
        # Check for valid characters (letters, numbers, hyphens, underscores)
        if not re.match(r'^@[a-zA-Z0-9_-]+$', username):
            print("❌ Invalid characters in Venmo username")
            return False
        
        return True
    
    def _validate_phone(self, phone: str) -> bool:
        """Validate phone number format (basic validation)"""
        # Remove common formatting characters
        clean_phone = re.sub(r'[^\d]', '', phone)
        
        if len(clean_phone) != 10:
            print("❌ Invalid phone number format (should be 10 digits)")
            return False
        
        return True
