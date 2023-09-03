from django.urls import path
from Hydrations.views import HomeView, AboutView, ContactView, CartView, CheckoutView,ContactFormView, VitaminGummiesView , edit_user_data, AddToCartView, Update_cart_view, RemoveItemView, EffervescentTabletsView, AyurvedicPowerView
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
    path('EffervescentTablets/', EffervescentTabletsView.as_view(), name='EffervescentTabletsView'),
    path('AyurvedicPower/', AyurvedicPowerView.as_view(), name='AyurvedicPower'),
    path('VitaminGummies/<slug:slug>', VitaminGummiesView.as_view(), name="SlugView"),
    path("user_data/", views.user_data_function, name= "user_data"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path('edit_user_data/',views.edit_user_data,name="edit_user_data"),
    path('initiate_payment/',views.homepage,name="initiate_payment"),
    path('initiate_payment/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('terms&conditions/', views.terms_conditions, name='terms&conditions'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('updateCart/', Update_cart_view.as_view(), name="update cart"),
    path('removeItem/', RemoveItemView.as_view(), name='removeItem'),

]