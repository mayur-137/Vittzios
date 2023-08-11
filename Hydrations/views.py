from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import UserRegistrationForm
from .models import VitaminGummies, EffervescentTablets, AyurvedicPower


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


class ContactView(FormView):
    template_name = "Contact.html"
    form_class = UserRegistrationForm
    success_url = "/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        contact = super().get_context_data()
        return contact


class CartView(TemplateView):
    template_name = "Cart.html"

    def get_context_data(self, **kwargs):
        cart = super().get_context_data()
        slug = self.kwargs.get("slug")
        print(slug)
        return cart


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
