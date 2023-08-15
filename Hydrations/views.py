from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from .forms import ContactFormModel, ProductBuyFormDetails
from .models import VitaminGummies, EffervescentTablets, AyurvedicPower, ContactModel, ProductBuyDetails


class VitaminGummiesView(TemplateView):
    model = VitaminGummies
    template_name = "VitaminGummies.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        VG["vg"] = VitaminGummies.objects.all()
        return VG


class HomeView(TemplateView):
    template_name = "Home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["VG"] = VitaminGummies.objects.all()
        context["ET"] = EffervescentTablets.objects.all()
        context["AP"] = AyurvedicPower.objects.all()
        return context


class AboutView(TemplateView):
    template_name = "About.html"

    def get_context_data(self, **kwargs):
        about = super().get_context_data()
        return about


class ContactView(TemplateView):
    template_name = "Contact.html"

    def get_context_data(self, **kwargs):
        contact = super().get_context_data()
        return contact


class ContactFormView(CreateView):
    model = ContactModel
    form_class = ContactFormModel
    template_name = "success.html"
    success_url = "/submit/"

    def form_valid(self, form):
        print(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("form invalid")
        return super().form_invalid(form)


class CartView(CreateView):
    model = ProductBuyDetails
    form_class = ProductBuyFormDetails
    template_name = "Cart.html"
    success_url = "/cart/"

    def form_valid(self, form):
        print("name", form.cleaned_data["email"])

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CheckoutView(TemplateView):
    model = VitaminGummies
    template_name = "Checkout.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        slug = self.kwargs.get("slug")
        VG["vg"] = VitaminGummies.objects.filter(slug=slug)
        if not VG["vg"]:
            VG["vg"] = EffervescentTablets.objects.filter(slug=slug)
        if not VG["vg"]:
            VG["vg"] = AyurvedicPower.objects.filter(slug=slug)
        return VG
