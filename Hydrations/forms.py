from django import forms


class ContactFormModel(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
