from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import Profile
from cart.models import Cart

user_model = get_user_model()


@receiver(post_save, sender=user_model)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=user_model)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.get_or_create(user=instance)