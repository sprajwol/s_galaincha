from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_address = models.CharField(max_length=50)
    permanent_address = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
