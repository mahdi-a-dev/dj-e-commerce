from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = "حساب ها"
    
    def ready(self):
        from accounts import signals
