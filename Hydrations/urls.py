from django.urls import path
from Hydrations.views import (HomeView, AboutView, ContactView, CartView, CartViewTemplateView, CheckoutView,
                              ContactFormView, VitaminGummiesView, AddToCartView, Update_cart_view, RemoveItemView,
                              EffervescentTabletsView, AyurvedicPowerView, user_datasobj, ResetView, LoginView,
                              VerifyOTPView, forget_password, reset_verified, forget_username,
                              RegisterView, ApplyPromoView, CashOnDelivery, SuccessPlacedOrder, SubscribeView)
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
    path('Subscribe/', SubscribeView.as_view(), name="SubscribeView"),
    path('EffervescentTablets/', EffervescentTabletsView.as_view(), name='EffervescentTabletsView'),
    path('AyurvedicPower/', AyurvedicPowerView.as_view(), name='AyurvedicPower'),
    path('VitaminGummies/<slug:slug>', VitaminGummiesView.as_view(), name="SlugView"),
    path('EffervescentTablets/<slug:slug>', VitaminGummiesView.as_view(), name="SlugView"),
    path('AyurvedicPower/<slug:slug>', VitaminGummiesView.as_view(), name="SlugView"),
    path("register/", RegisterView.as_view(), name="register"),
    path("user_data/", views.user_datasobj.user_data_function, name="user_data"),
    path('edit_user_data/', views.user_datasobj.edit_user_data, name="edit_user_data"),
    path('terms&conditions/', views.terms_conditions, name='terms&conditions'),
    path('Refund&policies/', views.Refund_policies, name='Refund&policies'),
    path('terms&conditions/', views.terms_conditions, name='terms&conditions'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('updateCart/', Update_cart_view.as_view(), name="update cart"),
    path('removeItem/', RemoveItemView.as_view(), name='removeItem'),
    path("register_verified/", VerifyOTPView.as_view(), name="register_verified"),
    path("forget_password/", forget_password.as_view(), name="register_verified"),
    path("reset_verified/", reset_verified.as_view(), name="reset_verified"),
    path("reset_password/", ResetView.as_view(), name="reset_passsowrd"),
    path("forget_username/", forget_username.as_view(), name="forget_username"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("promocode/", ApplyPromoView.as_view(), name="promo"),
    path("initiate_payment/", CashOnDelivery.as_view(), name="cod"),
    path("successDelivery/", SuccessPlacedOrder.as_view(), name="success")
]
