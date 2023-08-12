from django.urls import path
from Hydrations.views import HomeView, AboutView, ContactView, CartView, CheckoutView,ContactFormView, VitaminGummiesView

urlpatterns = [

    path('', HomeView.as_view(), name="index"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('cart/', CartView.as_view(), name="cart"),
    path('submit/', ContactFormView.as_view(), name="submit"),
    path('checkout/<slug:slug>', CheckoutView.as_view(), name="checkout"),
    path('VitaminGummies/', VitaminGummiesView.as_view(), name="ViitDB"),
    path('VitaminGummies/<slug:slug>', VitaminGummiesView.as_view(), name="SlugView"),

]