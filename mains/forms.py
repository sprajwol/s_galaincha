from django import forms
from login_system.models import Design
from django.contrib.auth.models import User


class Design_Form(forms.ModelForm):

    class Meta:
        model = Design
        fields = ('design_title', 'design_input', 'design_desc')
