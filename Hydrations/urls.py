from django.urls import path
from Hydrations.views import HomeView, AboutView, ContactView, CartView, CheckoutView,ContactFormView, VitaminGummiesView,user_data
from . import views
app_name = "main" 

urlpatterns = [

    path('', HomeView.as_view(), name="index"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('cart/', CartView.as_view(), name="cart"),
    path('submit/', ContactFormView.as_view(), name="submit"),
    path('checkout/<slug:slug>', CheckoutView.as_view(), name="checkout"),
    path('VitaminGummies/', VitaminGummiesView.as_view(), name="ViitDB"),
    path('VitaminGummies/<slug:slug>', VitaminGummiesView.as_view(), name="SlugView"),
    path("user_data/", views.user_data_function, name= "user_data"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
]