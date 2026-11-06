from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()

class Profile(models.Model):
    """
    Profile model contains user personal details
    """
    user = models.OneToOneField(
        user_model,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    email = models.EmailField(max_length=200, unique=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.phone_number} - {self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name_plural = "Profiles"
        ordering = ("-created",)