from django.forms import ModelForm
from .models import ContactModel, ProductBuyDetails


class ContactFormModel(ModelForm):
    class Meta:
        model = ContactModel
        fields = ["name", "email", "message"]


class ProductBuyFormDetails(ModelForm):
    class Meta:
        model = ProductBuyDetails
        fields = ['slug']
