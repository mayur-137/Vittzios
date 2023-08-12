from django import forms
from .models import ContactModel


class ContactFormModel(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'message']



