from django.views.generic.base import TemplateView
from .models import VitaminGummies, EffervescentTablets, AyurvedicPower


class VitaminGummiesView(TemplateView):
    model = VitaminGummies
    template_name = "VitaminGummies.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        # slug = self.kwargs.get("slug")
        # if slug is None:
        VG["vg"] = VitaminGummies.objects.all()
        # else:
        #     VG["vg"] = VitaminGummies.objects.filter(slug=slug)
        print(VG["vg"])
        if not VG["vg"]:
            return {"NF": "not found"}
        return VG


# class SlugDetailsView(DetailView):
#     model = VitaminGummies
#     template_name = "VitaminGummies.html"
#
#     def get_object(self, **kwargs):
#         slug = self.kwargs.get("slug")
#         VG["hi"] = VitaminGummies.objects.filter(slug=slug)
#         print(slug, VG, "77777777777777777777777")
#         return VG


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
    model = VitaminGummies
    template_name = "Checkout.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        slug = self.kwargs.get("slug")
        VG["vg"] = VitaminGummies.objects.filter(slug=slug)
        print(VG["vg"])
        if not VG["vg"]:
            return {"NF": "not found"}
        return VG
