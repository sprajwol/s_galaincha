from django import forms
from .models import Design


class Design_Form(forms.ModelForm):
    class Meta:
        model = Design
        fields = ('design_title', 'design_input', 'design_desc', )
