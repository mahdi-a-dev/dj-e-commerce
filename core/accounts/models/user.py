from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given phone number, and password.
        """
        if not phone_number:
            raise ValueError("Phone number is required")
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user


    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Creates and saves a superuser with the given phone number, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser True.")
        
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custome user model, verification with phone number
    """
    phone_number = PhoneNumberField(
        max_length=13,
        unique=True
    )
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
        
    USERNAME_FIELD = "phone_number"
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    def __str__(self):
        return self.phone_number.as_national
