from django import forms
from .models import ContactModel, subscribed_user
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import user_data

class ContactFormModel(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'message']


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

from django.forms import ModelForm
from .models import ContactModel

class ContactFormModel(ModelForm):
    class Meta:
        model = ContactModel
        fields = ["name", "email", "message"]



class SubscribeForm(forms.ModelForm):
    class Meta:
        model = subscribed_user
        fields = ["email"]