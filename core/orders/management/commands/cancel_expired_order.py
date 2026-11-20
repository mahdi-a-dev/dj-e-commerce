from django.core.management.base import BaseCommand
from orders.services import cancel_expireds

class Command(BaseCommand):
 
    def handle(self, *args, **options):
        cancel_expireds()
        
        self.stdout.write(
                self.style.SUCCESS("cancel_expired_order Command Worked Successfully.")
            )
        