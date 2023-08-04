from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django.views.generic.list import ListView
from .models import VitaminGummies, EffervescentTablets, AyurvedicPower


class VittList(ListView):
    model = VitaminGummies
    template_name = "VitaminGummies.html"

    def get_queryset(self, slug=None, *args, **kwargs):
        VG = VitaminGummies.objects.filter(slug=slug)
        print(VG, "VG00000000000000000000000000000000")
        return VG


class VitaminGummiesView(DetailView):
    model = VitaminGummies
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = "VitaminGummies.html"

    def get_queryset(self, *args, **kwargs):
        VG = VitaminGummies.objects.filter(slug="Mayurs")
        print(VG, "VG00000000000000000000000000000000")
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


class CartView(TemplateView):
    template_name = "Cart.html"

    def get_context_data(self, **kwargs):
        cart = super().get_context_data()
        return cart


class CheckoutView(TemplateView):
    template_name = "Checkout.html"

    def get_context_data(self, **kwargs):
        checkout = super().get_context_data()
        return checkout
