from django import forms
from .models import Design
from django.contrib.auth.models import User


class Design_Form(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput(), initial=User.username)

    class Meta:
        model = Design
        fields = ('user', 'design_title', 'design_input', 'design_desc')
