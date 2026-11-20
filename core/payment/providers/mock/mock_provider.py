from payment.models import Payment
from django.core.exceptions import ValidationError


class MockProvider:
    def process(self, selected_status):
        results = {
            "success": Payment.Status.SUCCESS,
            "failed": Payment.Status.FAILED
        }
        
        try:
            return results[selected_status]
        except KeyError:
            raise ValidationError("Invalid payment result.")

  
mock_provider = MockProvider()
