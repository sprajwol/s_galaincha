from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design_input = models.FileField(upload_to='inp_images/')
    design_title = models.CharField(
        max_length=40, blank=False, default="default")
    design_desc = models.CharField(max_length=255, blank=True)
    design_output = models.FileField(upload_to='out_images/', blank=True)
    design_output_txt = models.FileField(upload_to='out_txt/', blank=True)
    design_uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Design Gallery'
