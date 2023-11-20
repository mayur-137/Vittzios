import ast
import json
import random
import datetime
from django.utils import timezone
from datetime import timedelta, datetime
from math import ceil

import razorpay
import requests
from django.contrib import messages
from geopy.geocoders import Nominatim
from django.contrib.auth import logout
from django.contrib.auth.models import User, auth
from django.db.models import Max
from django.http import HttpResponseBadRequest, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.core.mail import EmailMessage
from django.views import View
from django.http import JsonResponse
from rest_framework.fields import empty

from .forms import ContactFormModel, SubscribeForm
from .models import VitaminGummies, EffervescentTablets, AyurvedicPower, ContactModel, user_data, orders, \
    final_order_list, user_email, subscribed_user, WishList, PromoCode, PromoCodeVerify, cart_data

from .configurations import email_content

current_date = datetime.now()

# Format the date
formatted_date = current_date.strftime("%d-%m-%Y")


def GetZIPtoState(zipcode):
    geolocator = Nominatim(user_agent="geoapiExercises")
    # Using geocode()
    location = geolocator.geocode(zipcode)
    return str(location)


class VitaminGummiesView(TemplateView):
    model = VitaminGummies
    template_name = "VitaminGummies.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        slug = self.kwargs.get("slug")
        VG["vg"] = VitaminGummies.objects.all()
        return VG


class EffervescentTabletsView(TemplateView):
    model = EffervescentTablets
    template_name = "EffervescentTablets.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        VG["vg"] = EffervescentTablets.objects.all()
        return VG


class AyurvedicPowerView(TemplateView):
    model = AyurvedicPower
    template_name = "AyurvedicPower.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        VG["vg"] = AyurvedicPower.objects.all()
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
    template_name = "cont_term/About.html"

    def get_context_data(self, **kwargs):
        about = super().get_context_data()
        return about


class MailView(View):
    email = "Vittzios <email>"
    signature = "\n\nBest Regards,\nVittzios"

    def send_email(self, subject, message, to_email):
        message += self.signature
        email = EmailMessage(subject, message, self.email, [to_email])
        email.send()

    @staticmethod
    def OtpGeneration():
        OTP = random.randint(100000, 999999)
        return OTP

    @staticmethod
    def Verification(request, email, user_otp):
        resetpassword_opt = request.session.get("otp")
        try:
            user = user_email.objects.get(email=email)
            otp = user.otp
        except Exception as e:
            print(e)

        if int(user_otp) == int(resetpassword_opt):
            return True
        else:
            return False


class SubscribeView(CreateView, MailView):
    model = subscribed_user
    form_class = SubscribeForm
    template_name = "cont_term/About.html"
    success_url = "/about/"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        subscribe_email_json = email_content.email_content
        subscribe_email_json_subject = subscribe_email_json["subscribe"]["subject"]
        subscribe_email_json_body = subscribe_email_json["subscribe"]["body"]
        message = f"""Dear {email}, \n
        {subscribe_email_json_body}
        """
        self.send_email(subscribe_email_json_subject, message, email)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ContactView(TemplateView):
    template_name = "cont_term/Contact.html"

    def get_context_data(self, **kwargs):
        contact = super().get_context_data()
        return contact


class ContactFormView(CreateView, MailView):
    model = ContactModel
    form_class = ContactFormModel
    template_name = "cont_term/Contact.html"
    success_url = "/contact/"

    def form_valid(self, form):
        contact = super().form_valid(form)
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]
        contact_email_json = email_content.email_content
        contact_email_json_subject = contact_email_json["contact_us"]["subject"]
        contact_email_json_body = contact_email_json["contact_us"]["body"]
        message = message + contact_email_json_body
        self.send_email(contact_email_json_subject, message, email)
        return contact

    def form_invalid(self, form):
        contact = super().form_invalid(form)
        return contact


class CartViewTemplateView(TemplateView):
    template_name = "cart_checkout/Cart.html"

    def get_context_data(self, **kwargs):
        cart = super().get_context_data()
        slug = self.kwargs.get("slug")
        return cart


class CheckoutView(TemplateView):
    model = VitaminGummies
    template_name = "cart_checkout/Checkout.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        slug = self.kwargs.get("slug")
        VG["vg"] = VitaminGummies.objects.filter(slug=slug)
        if not VG["vg"]:
            VG["vg"] = EffervescentTablets.objects.filter(slug=slug)
        if not VG["vg"]:
            VG["vg"] = AyurvedicPower.objects.filter(slug=slug)
        return VG


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        models = [VitaminGummies, EffervescentTablets, AyurvedicPower]
        for model in models:
            try:
                product = get_object_or_404(model, id=product_id)
                product = model.objects.filter(id=product_id)

            except Http404:
                pass
        cart_session = request.session.get('cart_session', {})
        for details in product:
            pass
        if cart_session.get(product_id) is None or cart_session.get(product_id) < details.max_quantity:
            cart_session[product_id] = cart_session.get(product_id, 0) + 1
            request.session['cart_session'] = cart_session
            request.session["discount_coupen"] = 0
            request.session["discounted_price_coupen"] = 0
            request.session["PromoMessage"] = f""
        if cart_session.get(product_id) == details.max_quantity:
            details.stock = False
            for model in models:
                try:
                    updateStock = model.objects.filter(id=product_id).update(stock=details.stock)
                except Exception as e:
                    print(e)
                    pass
        return redirect("/cart/")


class CartView(View):
    def get(self, request, *args, **kwargs):
        global email, c
        products_in_cart = []
        products_list = []
        product_total = 0
        cart = request.session.get('cart_session', {})
        try:
            discount_coupen = request.session["discount_coupen"]
            discounted_price_coupen = request.session["discounted_price_coupen"]
            promo_code_message = request.session["PromoMessage"]
            promocode = request.session["promocode"]
            minimum_amount_promo = request.session["minimum_amount_promo"]

        except Exception as e:
            discount_coupen = 0
            discounted_price_coupen = 0
            promo_code_message = 0
            print(e, "Promo error")

        models = [VitaminGummies, EffervescentTablets, AyurvedicPower]
        for model in models:
            try:
                itm = model.objects.filter(id__in=cart.keys())
                if itm:
                    products_in_cart.append(itm)
            except:
                pass
        for products in products_in_cart:
            for product in products:
                product.subtotal = product.price * cart[str(product.id)]
                product_total = product.subtotal + product_total
                product.product_quantity = str(cart[str(product.id)])
                products_list.append(product)

        try:
            email = request.user.email
            order_product_data = []
            for i in products_list:
                quantity = i.product_quantity
                products_detail = str(str(i.id) + "#" + str(i.name) + "#" + str(quantity) + "#" + (str(i.price)))
                order_product_data.append(products_detail)

            try:
                c = user_data.objects.get(email=email)
                address = str(c.building) + " , " + str(c.street) + " , " + str(c.area) + " , " + str(
                    c.pincode) + " , " + str(c.city)

                if discounted_price_coupen == 0:
                    discounted_price_coupen = product_total
                elif product_total <= minimum_amount_promo:
                    discount_coupen = 0
                    discounted_price_coupen = product_total
                else:
                    pass

                if orders.objects.filter(email=email).exists():
                    if order_product_data != "":
                        user = orders.objects.get(email=email)
                        user.products_detail = order_product_data
                        user.order_total = discounted_price_coupen
                        user.address_1 = address
                        user.save()
                    else:
                        pass
                else:
                    if order_product_data != "":
                        b = orders(email=email, address_1=address, products_detail=order_product_data,
                                   order_total=product_total)
                        orders.save(b)
                    else:
                        pass

                return render(request, 'cart_checkout/Cart.html',
                              {'products': products_list, 'product_total': product_total,
                               "PromoMessage": promo_code_message, "discount": discount_coupen,
                               "discounted_price": discounted_price_coupen})

            except Exception as e:
                print(e, "ee")
                context = "you have to add your address first"
                print("you have to add your address first")
                messages.success(request, context)
                return redirect('/edit_user_data/', {"context": context, "request": "post"})

        except:
            context = "you have to register first"
            messages.success(request, context)
            return redirect('/register/', {"context": context})


class Update_cart_view(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.GetMaxQuantity = None

    def post(self, request, *args, **kwargs):
        Product_id = request.POST.get("Update_product_quantity")
        Mode_of_Operations = request.POST.get("minus")
        models = [VitaminGummies, EffervescentTablets, AyurvedicPower]
        for model in models:
            try:
                product = model.objects.filter(id=Product_id)
                for details in product:
                    pass
            except:
                pass
        if Mode_of_Operations == "-":
            cart_session = request.session.get('cart_session', {})
            cart_session[Product_id] = cart_session.get(Product_id) - 1
            request.session['cart_session'] = cart_session
            request.session["discount_coupen"] = 0
            request.session["discounted_price_coupen"] = 0
            request.session["PromoMessage"] = f""
            if cart_session.get(Product_id) < details.max_quantity:
                details.stock = True
                for model in models:
                    try:
                        updateStock = model.objects.filter(id=Product_id).update(stock=details.stock)
                    except:
                        pass
            elif details.max_quantity == 0:
                details.stock = False
                for model in models:
                    try:
                        updateStock = model.objects.filter(id=Product_id).update(stock=details.stock)
                    except:
                        pass
            if cart_session.get(Product_id) == 0 or details.max_quantity == 0:
                del cart_session[Product_id]
        else:
            cart_session = request.session.get('cart_session', {})
            if not cart_session.get(Product_id) == details.max_quantity:
                cart_session[Product_id] = cart_session.get(Product_id) + 1
                request.session['cart_session'] = cart_session
                request.session["discount_coupen"] = 0
                request.session["discounted_price_coupen"] = 0
                request.session["PromoMessage"] = f""
            else:
                details.stock = False
                for model in models:
                    try:
                        updateStock = model.objects.filter(id=Product_id).update(stock=details.stock)
                    except:
                        pass
        return redirect("/cart/")


class RemoveItemView(View):
    def post(self, request, *args, **kwargs):
        GetRemoveItemId = request.POST.get("removeItem")
        cart_session = request.session.get('cart_session', {})
        models = [VitaminGummies, EffervescentTablets, AyurvedicPower]
        for model in models:
            try:
                product = model.objects.filter(id=GetRemoveItemId)
                for details in product:
                    pass
            except:
                pass
        if details.stock == False:
            details.stock = True
            for model in models:
                try:
                    updateStock = model.objects.filter(id=GetRemoveItemId).update(stock=details.stock)
                except:
                    pass
        if GetRemoveItemId in cart_session:
            del cart_session[GetRemoveItemId]
            request.session['cart_session'] = cart_session
            request.session["discount_coupen"] = 0
            request.session["discounted_price_coupen"] = 0
            request.session["PromoMessage"] = f""
        return redirect("/cart/")


class user_datas:

    def user_data_function(self, request):
        try:
            email = request.user.email
            try:
                print("user data already stored ")
                username = (User.objects.get(email=email)).username
                phone_number = user_data.objects.get(email=email).phone_number
                building = user_data.objects.get(email=email).building
                street = (user_data.objects.get(email=email)).street
                area = (user_data.objects.get(email=email)).area
                pincode = (user_data.objects.get(email=email)).pincode
                city = (user_data.objects.get(email=email)).city
                state = (user_data.objects.get(email=email)).state
                context = {"email": email, "phone_number": phone_number, 'username': username, 'building': building,
                           'street': street, 'area': area, 'pincode': pincode, 'city': city, 'state': state}

                request.session['edit_redirect'] = "user_data"
                return render(request, 'user_data/user_data.html', {'context': context})

            except:
                return render(request, 'user_data/user_data.html')
        except:
            print('no user found')
            return redirect('/login/', {"context": "you have't logged in "})

    @csrf_exempt
    def edit_user_data(self, request):
        email = request.user.email
        if request.method == "GET":
            try:
                building = request.GET['building']
                street = request.GET['street']
                area = request.GET['area']
                pincode = request.GET['pincode']
                city = request.GET['city']
                state = request.GET['state']
                phone_number = request.GET['phone_number']
                address = str(
                    str(building) + ',' + str(street) + ',' + str(area) + ',' + str(pincode) + ',' + str(
                        city) + ',' + str(
                        state) + ',' + str(phone_number))

                if orders.objects.filter(email=email).exists():
                    user = orders.objects.filter(email=request.user.email).update(address_1=address)
                else:
                    b = orders(email=email, address_1=address)
                    orders.save(b)

                if user_data.objects.filter(email=email).exists():
                    print("your data is saved")
                    user = user_data.objects.get(email=email)
                    user.building = building
                    user.street = street
                    user.area = area
                    user.pincode = pincode
                    user.city = city
                    user.phone_number = phone_number
                    user.state = state
                    user.save()
                else:
                    b = user_data(email=email, building=building, street=street, area=area, pincode=pincode, city=city,
                                  phone_number=phone_number, state=state)
                    user_data.save(b)

                    return redirect('/')

                edit_change = request.session.get('edit_redirect')
                return redirect('/{}/'.format(edit_change))
            except Exception as e:
                print(e, "e")
                return render(request, 'user_data/edit_user_data.html')


        else:
            return render(request, 'user_data/edit_user_data.html')


user_datasobj = user_datas()


class RemoveWishListItem(View):

    def post(self, request, *args, **kwargs):
        RemoveWishItem_id = request.POST.get("removeWishListItem")
        try:
            addFavItem = WishList.objects.filter(product_id=RemoveWishItem_id).delete()
        except Exception as e:
            print(e)
        return redirect("/wishlist/")


class ApplyPromoView(View):
    model = PromoCode
    template_name = "cart_checkout/Cart.html"

    def post(self, request, *args, **kwargs):
        user = request.user
        All_promos = PromoCode.objects.all()
        GetPromo = request.POST.get("code")
        GetDiscount = int(request.POST.get("discount_coupen"))
        for promo in All_promos:
            try:
                if GetPromo == promo.code:
                    if int(GetDiscount) >= promo.min_amount:
                        if not PromoCodeVerify.objects.filter(email=user.email).exists():
                            discounted_price_coupen = GetDiscount - promo.discount
                            request.session["promocode"] = promo.code
                            request.session["discount_coupen"] = promo.discount
                            request.session["discounted_price_coupen"] = discounted_price_coupen
                            request.session["minimum_amount_promo"] = promo.min_amount
                            request.session["PromoMessage"] = f"Congratulations, Your Coupon Code {promo.code} Applied."

                            return redirect("/cart/")
                        else:
                            request.session["promocode"] = promo.code
                            request.session["discount_coupen"] = 0
                            request.session["discounted_price_coupen"] = 0
                            request.session["minimum_amount_promo"] = promo.min_amount
                            request.session[
                                "PromoMessage"] = f"Your Coupon Code Not Applied, Because you have a already applied {promo.code}"
                            return redirect("/cart/")
                    else:
                        request.session["promocode"] = promo.code
                        request.session["discount_coupen"] = 0
                        request.session["discounted_price_coupen"] = 0
                        request.session["minimum_amount_promo"] = promo.min_amount
                        request.session[
                            "PromoMessage"] = (f"Your Coupon Code Not Applied, Add {promo.min_amount - GetDiscount} to "
                                               f"Applied.")

                        return redirect("/cart/")
                else:
                    request.session["discount_coupen"] = 0
                    request.session["promocode"] = promo.code
                    request.session["discounted_price_coupen"] = 0
                    request.session["minimum_amount_promo"] = 0
                    request.session["PromoMessage"] = f"Promo code {GetPromo} dose not exits."

                    return redirect("/cart/")
            except Exception as e:
                print(e, "set promo")
                return redirect("/cart/")


class RegisterView(MailView):

    def get(self, request):
        return render(request, 'login/register.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            context = {"error": "this email or username is already taken try another one"}
            return render(request, 'login/register.html', {"context": context})
        else:
            otp = self.OtpGeneration()
            OTP_email_json = email_content.email_content
            OTP_email_json_subject = OTP_email_json["OTP_Send"]["subject"]
            OTP_email_json_body1 = OTP_email_json["OTP_Send"]["body1"]
            OTP_email_json_body2 = OTP_email_json["OTP_Send"]["body2"]
            message = OTP_email_json_body1 + f"\nYour OTP: {otp}\n" + OTP_email_json_body2
            self.send_email(OTP_email_json_subject, message, email)

            # Store the OTP and timestamp in the session
            request.session['username'] = username
            request.session['password'] = password
            request.session['email'] = email
            request.session['otp'] = otp
            request.session['otp_timestamp'] = str(timezone.now())

            return redirect('/register_verified/')


class LoginView(View):

    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request, *args, **kwargs):
        try:
            email = request.POST['email_address']
            password = request.POST['password']
        except Exception as e:
            print(e, "ee")
        try:
            username = User.objects.get(email=email)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                context = {'error': 'email and password does not match.'}
                return render(request, 'login/login.html', {'context': context})
        except:
            context = {'error': 'user not found go to register'}
            return render(request, 'login/register.html', {'context': context})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


class ResetView(MailView):

    def get(self, request, *args, **kwargs):
        if request.session.get('otp_verified'):
            return render(request, "login/reset_password.html")
        else:
            context = "you need verify via otp first"
            return render(request, 'login/forget.html', {'context': context})

    def post(self, request, *args, **kwargs):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.session.get("reset_email")
        if password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                success_reset_passwd_email_json = email_content.email_content
                success_reset_passwd_email_json_subject = success_reset_passwd_email_json["successfullyResetPassword"][
                    "subject"]
                success_reset_passwd_email_json_body = success_reset_passwd_email_json["successfullyResetPassword"][
                    "body"]
                message = f"\nDear {user},\n\n" + success_reset_passwd_email_json_body
                self.send_email(success_reset_passwd_email_json_subject, message, email)
                return redirect('/login/')
            except Exception as e:
                print(e, "ee")
                if "User matching query does not exist" in str(e):
                    context = "Email Not Found, Please Register First."
                    return render(request, 'login/reset_password.html', {'context': context})
                else:
                    context = "Please Try Again !!"
                    return render(request, 'login/reset_password.html', {'context': context})
        else:
            context = "enter same password"
            return render(request, 'login/reset_password.html', {'context': context})


class reset_verified(MailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'login/verification.html')

    def post(self, request, *args, **kwargs):
        reset_email = request.session.get("reset_email")
        user_otp = request.POST['otp']
        site = self.Verification(request, reset_email, user_otp)
        request.session['otp_verified'] = True
        if site:
            print("reset_password")
            return redirect('/reset_password/')
        else:
            print("reset_password fail")
        site = '/reset_verified/'
        return render(request, 'login/verification.html', {'site': site})


class VerifyOTPView(MailView):

    def get(self, request):
        return render(request, 'login/verification.html')

    def post(self, request):
        user_otp = request.POST.get('otp')
        a = request.session.get('otp')
        otp_timestamp_str = request.session.get('otp_timestamp')

        if otp_timestamp_str:
            otp_timestamp = datetime.strptime(otp_timestamp_str, "%Y-%m-%d %H:%M:%S.%f%z")

            # Check if the OTP has expired (more than 60 seconds old)
            if timezone.now() > otp_timestamp + timedelta(seconds=60):
                context = {"error": "The OTP has expired. Please try again."}
                return render(request, 'login/register.html', {"context": context})

            # Check if the entered OTP matches the one in the session
            if int(user_otp) == int(request.session.get('otp')):
                username = request.session.get('username')
                password = request.session.get('password')
                email = request.session.get('email')

                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                Register_email_content = email_content.email_content
                Register_email_content_subject = Register_email_content["Register"]["subject"]
                Register_email_content_body = Register_email_content["Register"]["body"]
                message = f"""Dear {username},
                 {Register_email_content_body}
                """
                self.send_email(Register_email_content_subject, message, email)

                return redirect("/login/")

        context = "Invalid OTP. Please try again."
        return render(request, 'login/verification.html', {"context": context})


class forget_password(MailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'login/forget.html')

    def post(self, request, *args, **kwargs):
        current_email = request.POST['email']
        try:
            user_username = (User.objects.get(email=current_email)).password
            otp = self.OtpGeneration()
            OTP_email_json = email_content.email_content
            OTP_email_json_subject = OTP_email_json["ResetPassword"]["subject"]
            OTP_email_json_body1 = OTP_email_json["ResetPassword"]["body1"]
            OTP_email_json_body2 = OTP_email_json["ResetPassword"]["body2"]
            message = OTP_email_json_body1 + f"\nYour One-Time Password (OTP) for resetting your password is: {otp}. Please use this OTP to proceed with resetting your password.\n\n" + OTP_email_json_body2
            self.send_email(OTP_email_json_subject, message, current_email)

            request.session['otp'] = otp
            request.session['otp_timestamp'] = str(timezone.now())
            request.session["reset_email"] = current_email

            request.session["reset_email"] = current_email
            return redirect('/reset_verified/')
        except Exception as e:
            print(e, "reset e")
            context = "Your Email Dose Not Exist, Please Register First."
            return render(request, 'login/forget.html', {"messages": context})


class forget_username(MailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'login/forget_username.html')

    def post(self, request, *args, **kwargs):
        current_email = request.POST['email']
        try:
            user_username = (User.objects.get(email=current_email)).username
            username_email_json = email_content.email_content
            username_email_json_subject = username_email_json["RetriveUsername"]["subject"]
            username_email_json_body1 = username_email_json["RetriveUsername"]["body1"]
            username_email_json_body2 = username_email_json["RetriveUsername"]["body2"]
            message = username_email_json_body1 + f"\n\nYour username for your account is: {user_username}\n\n" + username_email_json_body2
            self.send_email(username_email_json_subject, message, current_email)
            self.send_email(username_email_json_subject, message, current_email)
            context = "Your Username Will Send Via Your Mail Please Check It."
            return render(request, 'login/forget_username.html', {'messages': context})
        except:
            context = "Your Email Dose Not Exits !!"
            return render(request, 'login/forget_username.html', {'messages': context})


@csrf_exempt
def terms_conditions(request):
    if request.method:
        return render(request, 'cont_term/terms_conditions.html')
    else:
        return redirect("/")


@csrf_exempt
def Refund_policies(request):
    if request.method:
        return render(request, 'cont_term/Refund_policies.html')
    else:
        return redirect("/")


class CashOnDelivery(MailView):

    def get(self, request, *args, **kwargs):
        otp = self.OtpGeneration()
        confirmationOrder_email_content = email_content.email_content
        confirmationOrder_email_content_subject = confirmationOrder_email_content["confirmationOrder"][
            "subject"]
        confirmationOrder_email_content_body1 = confirmationOrder_email_content["confirmationOrder"]["body1"]
        confirmationOrder_email_content_body2 = confirmationOrder_email_content["confirmationOrder"]["body2"]
        message = f"""Dear {request.user},\n

{confirmationOrder_email_content_body1}

Your OTP is {otp}. It is valid for 1 minutes. Please do not share it with anyone.

{confirmationOrder_email_content_body2}
                        """
        self.send_email(confirmationOrder_email_content_subject, message, request.user.email)
        request.session['otp'] = otp
        request.session['otp_timestamp'] = str(timezone.now())
        return render(request, "order.html")


class SuccessPlacedOrder(CashOnDelivery):

    def post(self, request):
        f = []
        user_otp = request.POST.get('otp')
        a = request.session.get('otp')
        otp_timestamp_str = request.session.get('otp_timestamp')

        user_cart_fill = orders.objects.get(email=request.user.email)

        if otp_timestamp_str:
            otp_timestamp = datetime.strptime(otp_timestamp_str, "%Y-%m-%d %H:%M:%S.%f%z")

            # Check if the OTP has expired (more than 90 seconds old)
            if timezone.now() > otp_timestamp + timedelta(seconds=300):
                context = {"error": "The OTP has expired. Please try again."}
                return redirect("/cart/")

            # Check if the entered OTP matches the one in the session
            if int(user_otp) == int(a):
                res = shipmentobj.shiprockeet_order_function(request=request)
                successfullyPlaced_email_content = email_content.email_content
                successfullyPlaced_email_content_subject = successfullyPlaced_email_content["successfullyOrderPlaced"][
                    "subject"]
                successfullyPlaced_email_content_body = successfullyPlaced_email_content["successfullyOrderPlaced"][
                    "body"]
                message = f"""Dear {request.user},\n

{successfullyPlaced_email_content_body}

Your order ID is {request.session["order_id"]}. You can use this ID to track your order status, delivery date, and other details on our website or app.

We hope you enjoy your purchase and have a wonderful day!
                """
                self.send_email(successfullyPlaced_email_content_subject, message, request.user.email)

                try:
                    if res["status"] == "NEW":
                        request.session["statusPayment"] = True
                        prdItems = user_cart_fill.products_detail.split(",")
                        order_total = user_cart_fill.order_total
                        Discount = 0
                        for i in range(len(prdItems)):
                            if "['" in prdItems[i].split("#")[0] or "'" in prdItems[i].split("#")[0]:
                                pID = prdItems[i].split("#")[0].split("'")[1]

                                prdData = VitaminGummies.objects.get(id=pID)
                                if "'" in prdItems[i].split("#")[3] or "']" in prdItems[i].split("#")[3]:
                                    prdData.subtotal = prdItems[i].split("#")[3].split("'")[0]

                                Discount = request.session["discount_coupen"]
                                prdData.quantity = prdItems[i].split("#")[2]
                                prdData.subtotal = int(prdData.subtotal) * int(prdData.quantity)
                                prdData.max_quantity = prdData.max_quantity - int(prdItems[i].split("#")[2])
                                prdData.save()
                                f.append(prdData)
                        request.session["discount_coupen"] = 0
                        request.session["discounted_price_coupen"] = 0
                        request.session["PromoMessage"] = f""
                        try:
                            if request.session["statusPayment"]:
                                PromoCodeVerify(code=request.session["promocode"], email=request.user.email).save()
                        except Exception as e:
                            print(e)
                    else:
                        request.session["statusPayment"] = False
                except Exception as e:
                    print(e)
                return render(request, "successfully_placed.html", {"Order": f, "UserAddress": user_cart_fill.address_1,
                                                                    "orderID": request.session["order_id"],
                                                                    "order_total": order_total, "Discount": Discount})
                # return redirect("/cart")

        context = "Invalid OTP. Please try again."
        return redirect("/cart/")


"""shipment code """


class shipment:
    def take_user_data(self, request):
        email = request.user.email
        username = request.user
        order_items_list = []
        # take billing data ffrom user_data table and order data table
        user = user_data.objects.get(email=email)
        user_billing_city = user.city
        user_billing_pincode = user.pincode
        user_billing_state = user.state
        user_billing_email = email
        user_billing_phone = user.phone_number

        # take cart data
        order_user = orders.objects.get(email=email)

        order_address = order_user.address_1

        if request.session["discounted_price_coupen"]:
            order_total = request.session["discounted_price_coupen"]
            discount_order_total = request.session["discount_coupen"]
        else:
            order_total = order_user.order_total
            discount_order_total = 0

        order_product = ast.literal_eval(order_user.products_detail)

        # add value to final order list
        b = final_order_list(email=email, address=order_address, products_detail=order_product, order_total=order_total,
                             shiprocket_dashboard=False)
        final_order_list.save(b)
        order_id = final_order_list.objects.aggregate(Max('order_id'))['order_id__max']
        # order_id =  final_order_list.objects.get(email=email AND adress=order_address)

        request.session["order_id"] = order_id

        prdItems = order_user.products_detail.split(",")
        for i in range(len(prdItems)):
            if "['" in prdItems[i].split("#")[0] or "'" in prdItems[i].split("#")[0]:
                pID = prdItems[i].split("#")[0].split("'")[1]

                prdData = VitaminGummies.objects.get(id=pID)
                if "'" in prdItems[i].split("#")[3] or "']" in prdItems[i].split("#")[3]:
                    prdData.subtotal = prdItems[i].split("#")[3].split("'")[0]
                prdData.quantity = prdItems[i].split("#")[2]
                order_items = {
                    "name": prdData.name,
                    "sku": str(prdData.id),
                    "units": prdData.quantity,
                    "selling_price": prdData.subtotal,
                    "discount": discount_order_total,
                    "tax": "",
                    "hsn": 441122
                }
                order_items_list.append(order_items)

        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M")
        order_data = {
            "order_id": order_id,
            "order_date": formatted_now,
            "pickup_location": "Primary",
            "channel_id": "4478346",
            "comment": "Reseller: Vittzios",
            "billing_customer_name": str(username),
            "billing_last_name": "",
            "billing_address": order_address,
            "billing_address_2": "",
            "billing_city": user_billing_city,
            "billing_pincode": user_billing_pincode,
            "billing_state": "Gujarat",
            "billing_country": "India",
            "billing_email": user_billing_email,
            "billing_phone": user_billing_phone,
            "shipping_is_billing": True,
            "shipping_customer_name": "",
            "shipping_last_name": "",
            "shipping_address": "",
            "shipping_address_2": "",
            "shipping_city": "",
            "shipping_pincode": "",
            "shipping_country": "",
            "shipping_state": "",
            "shipping_email": "",
            "shipping_phone": "",
            "order_items": order_items_list,
            "payment_method": "COD",
            "shipping_charges": 0,
            "giftwrap_charges": 0,
            "transaction_charges": 0,
            "total_discount": 0,
            "sub_total": order_total,
            "length": 10,
            "breadth": 15,
            "height": 20,
            "weight": 2.5
        }
        return order_data

    def shiprocket_key(self):
        url = "https://apiv2.shiprocket.in/v1/external/auth/login"
        headers = {
            "Content-Type": "application/json"}
        response = requests.post(url, json={
            "email": "Order.wholesomenutritech@gmail.com",
            "password": "bhoomi2510"}, headers=headers)
        a = response.json()
        return a['token']

    def shiprockeet_order_function(self, request):
        url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"

        api_key = self.shiprocket_key()
        print(api_key, "keys")
        headers = {
            "Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

        order_data = self.take_user_data(request=request)

        response = requests.post(url, json=order_data, headers=headers)

        return response.json()


shipmentobj = shipment()
