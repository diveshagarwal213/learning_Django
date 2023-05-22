from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from .managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

    MEMBERSHIP_CUSTOMER = "C"
    MEMBERSHIP_SELLER = "S"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_CUSTOMER, "Customer"),
        (MEMBERSHIP_SELLER, "Seller"),
    ]
    user_type = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_CUSTOMER
    )
    phone_number = models.CharField(max_length=15, unique=True)

    # USERNAME_FIELD='phone_number'
    # objects = CustomUserManager()


class VerifyPhoneNumber(models.Model):
    phone_number = models.CharField(
        max_length=15,
    )

    OTP = models.CharField(
        max_length=6,
    )
    OTP_NEW_ACCOUNT = "N"
    OTP_CHOICES = [
        (OTP_NEW_ACCOUNT, "NEW_ACCOUNT"),
    ]
    OTP_for = models.CharField(max_length=1, choices=OTP_CHOICES)

    expire_at = models.DateTimeField()
