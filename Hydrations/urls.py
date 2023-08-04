from django.urls import path
from Hydrations.views import HomeView, AboutView, ContactView, CartView, CheckoutView, VittList, VitaminGummiesView

urlpatterns = [

    path('', HomeView.as_view(), name="index"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('cart/', CartView.as_view(), name="cart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    # path('<slug:slug>/', HomeView.as_view()),
    path('VitaminGummies/<slug:slug>', VitaminGummiesView.as_view(), name="ViitDB"),

]