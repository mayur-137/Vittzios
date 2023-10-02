from django.urls import path
from Hydrations.views import HomeView, AboutView, ContactView, CartView, CartViewTemplateView, CheckoutView,ContactFormView, VitaminGummiesView , AddToCartView, Update_cart_view, RemoveItemView, EffervescentTabletsView, AyurvedicPowerView
from . import views
app_name = "main" 

urlpatterns = [
    path('test/', HomeView.as_view(), name="index"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('cart/', CartView.as_view(), name="cart"),
    path('submit/', ContactFormView.as_view(), name="submit"),
    path('checkout/<slug:slug>', CheckoutView.as_view(), name="checkout"),
    path('VitaminGummies/', VitaminGummiesView.as_view(), name="ViitDB"),
    path('EffervescentTablets/', EffervescentTabletsView.as_view(), name='EffervescentTabletsView'),
    path('AyurvedicPower/', AyurvedicPowerView.as_view(), name='AyurvedicPower'),
    path('VitaminGummies/<slug:slug>', VitaminGummiesView.as_view(), name="SlugView"),
    path('EffervescentTablets/<slug:slug>', VitaminGummiesView.as_view(), name="SlugView"),
    path('AyurvedicPower/<slug:slug>', VitaminGummiesView.as_view(), name="SlugView"),
    path("register/", views.login_register.register_request, name="register"),
    path("login/", views.login_register.login_request, name="login"),
    path("logout/", views.login_register.logout_request, name= "logout"),
    path("forget_password/", views.reset.forget_password, name= "register_verified"),
    path("register_verified/", views.reset.register_verified, name= "register_verified"),
    path("reset_verified/", views.reset.reset_verified, name= "reset_verified"),
    path("reset_password/", views.reset.reset_passsowrd, name= "reset_passsowrd"),
    path("forget_username/", views.reset.forget_username, name= "forget_username"),
    path("user_data/", views.user_datas.user_data_function, name= "user_data"),
    path('edit_user_data/',views.user_datas.edit_user_data,name="edit_user_data"),
    path('initiate_payment/',views.razor_payment.homepage,name="initiate_payment"),
    path('initiate_payment/paymenthandler/', views.razor_payment.paymenthandler, name='paymenthandler'),
    path('terms&conditions/', views.terms_conditions, name='terms&conditions'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('updateCart/', Update_cart_view.as_view(), name="update cart"),
    path('removeItem/', RemoveItemView.as_view(), name='removeItem'),

]