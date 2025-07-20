from typing import List, Optional
from datetime import datetime
from PaymentStrategy import PaymentStrategy

class PaymentProcessor:
    def __init__(self, payment_strategy: Optional[PaymentStrategy] = None):
        self._payment_strategy = payment_strategy
        self.payment_history: List[dict] = []
    
    def set_payment_strategy(self, payment_strategy: PaymentStrategy) -> None:
        self._payment_strategy = payment_strategy
        print(f"💰 Payment method set to: {payment_strategy.get_payment_method_name()}")
    
    def process_payment(self, amount: float, payment_info: dict) -> dict:
        if not self._payment_strategy:
            raise ValueError("No payment strategy set. Please select a payment method.")
        
        if not self._payment_strategy.validate_payment_info(payment_info):
            return {
                'success': False,
                'error': 'Invalid payment information',
                'payment_method': self._payment_strategy.get_payment_method_name()
            }
        
        result = self._payment_strategy.process_payment(amount, payment_info)
        self.payment_history.append({
            'timestamp': datetime.now(),
            'amount': amount,
            'result': result
        })
        return result
    
    def get_available_payment_methods(self) -> List[str]:
        return ["Credit Card", "Venmo", "PayPal"]
    
    def get_payment_history(self) -> List[dict]:
        return self.payment_history