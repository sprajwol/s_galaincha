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


class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designs_input = models.FileField(upload_to='inp_images/')
    designr_title = models.CharField(
        max_length=40, blank=False, default="default")
    designs_output = models.FileField(upload_to='out_images/', blank=True)
    designs_results = models.CharField(max_length=255, blank=True)
    designr_uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Design Gallery'
