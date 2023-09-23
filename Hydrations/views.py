from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views import View
from .forms import ContactFormModel
from .models import VitaminGummies, EffervescentTablets, AyurvedicPower, ContactModel, user_data, orders, \
    final_order_list
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import login, authenticate, logout  # add this
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactFormModel, NewUserForm
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from razorpay import Client
import razorpay, requests
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
import json
import ast

class VitaminGummiesView(TemplateView):
    model = VitaminGummies
    template_name = "VitaminGummies.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        slug = self.kwargs.get("slug")
        print(slug, "slug")
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
    template_name = "About.html"

    def get_context_data(self, **kwargs):
        about = super().get_context_data()
        return about


class ContactView(TemplateView):
    template_name = "Contact.html"

    def get_context_data(self, **kwargs):
        contact = super().get_context_data()
        return contact


class ContactFormView(CreateView):
    model = ContactModel
    form_class = ContactFormModel
    template_name = "success.html"
    success_url = "/submit/"

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CartViewTemplateView(TemplateView):
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


class ContactView(TemplateView):
    template_name = "Contact.html"

    def get_context_data(self, **kwargs):
        contact = super().get_context_data()
        return contact


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
        if cart_session.get(product_id) == None or cart_session.get(product_id) < details.max_quantity:
            cart_session[product_id] = cart_session.get(product_id, 0) + 1
            request.session['cart_session'] = cart_session
        if cart_session.get(product_id) == details.max_quantity:
            details.stock = False
            for model in models:
                try:
                    updateStock = model.objects.filter(id=product_id).update(stock=details.stock)
                except:
                    pass
        return redirect("/cart/")


class CartView(View):
    def get(self, request, *args, **kwargs):
        global email, c
        products_in_cart = []
        products_list = []
        # products_list.clear()
        product_total = 0
        cart = request.session.get('cart_session', {})
        print(cart, "3")

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
            print(email, "email")
            order_product_data = []
            for i in products_list:
                quantity = i.product_quantity
                print(i.name)
                products_detail = str(str(i.name) + "-" + str(quantity))
                order_product_data.append(products_detail)
                # order_product_data += str(","+products_detail + "\n")
            print(order_product_data)
            try:
                c = user_data.objects.get(email=email)
                print(c, "cccccccccc")
            except Exception as e:
                print(e, "eeeeeeee")
            address = str(c.building) + " , " + str(c.street) + " , " + str(c.area) + " , " + str(c.pincode) + " , " + str(c.city)
            if orders.objects.filter(email=email).exists():
                if order_product_data != "":
                    print("user data is there")
                    user = orders.objects.get(email=email)
                    user.products_detail = json.dumps(order_product_data)
                    user.order_total = orders.objects.get(email=email)
                    print(address)
                    user.address_1 = address
                    user.save()
                    print("user data changged")
                else:
                    entry = orders.objects.get(email=email)
                    entry.delete()
                    print("entry deleted")
            else:
                if order_product_data != "":
                    print("user data is not there")
                    b = orders(order_id=1, email=email, address_1=address, products_detail=order_product_data,
                            order_total=product_total)
                    orders.save(b)
                    print("user data saved")
                else:
                    pass

            return render(request, 'Cart.html', {'products': products_list, 'product_total': product_total})

        except Exception as e:
            return render(request, 'Cart.html')
        

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
            if cart_session.get(Product_id) < details.max_quantity:
                details.stock = True
                for model in models:
                    try:
                        updateStock = model.objects.filter(id=Product_id).update(stock=details.stock)
                    except:
                        pass
            if cart_session.get(Product_id) == 0:
                del cart_session[Product_id]
        else:
            cart_session = request.session.get('cart_session', {})
            if not cart_session.get(Product_id) == details.max_quantity:
                cart_session[Product_id] = cart_session.get(Product_id) + 1
                request.session['cart_session'] = cart_session
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
        return redirect("/cart/")


def user_data_function(request):
    current_user = request.user
    email = current_user.email
    if email:
        try:
            print("user already stored data")
            username = (User.objects.get(email=email)).username
            print(username)
            phone_number = user_data.objects.get(email=email).phone_number
            building = user_data.objects.get(email=email).building
            print(building)
            street = (user_data.objects.get(email=email)).street
            area = (user_data.objects.get(email=email)).area
            pincode = (user_data.objects.get(email=email)).pincode
            city = (user_data.objects.get(email=email)).city
            state = (user_data.objects.get(email=email)).state
            context = {"email": email, "phone_number": phone_number, 'username': username, 'building': building,
                       'street': street, 'area': area, 'pincode': pincode, 'city': city, 'state': state}
            print(context)
            return render(request, 'main/user_data.html', {'context': context})

        except:
            return render(request, 'main/user_data.html')
    else:
        return render(request, 'main/user_data.html')


@csrf_exempt
def edit_user_data(request):
    print("edit user data")
    if request.method == "POST":
        print("edit user data222")
        current_user = request.user
        email = current_user.email
        building = request.POST['building']
        street = request.POST['street']
        area = request.POST['area']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        phone_number = request.POST['phone_number']

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
            print("user data is not saved")
            b = user_data(email=email, building=building, street=street, area=area, pincode=pincode, city=city,
                          phone_number=phone_number, state=state)
            user_data.save(b)
        return redirect('login')
    else:
        print("GET")
        return render(request, 'main/edit_user_data.html')


@csrf_exempt
def register_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        print(username, email, password)
        if User.objects.filter(username=username).exists():
            print("user already registered")
            context = {'error': 'The username you entered has already been taken. Please try another username.'}
            return render(request, 'main/register.html', {'context': context})
        elif User.objects.filter(email=email).exists():
            print("this email is already taken try another one")
            context = {"error": "this email is already taken try another one"}
            return render(request, 'main/register.html', {"context": context})
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            print("user created")
            # context = {'error': 'User registered successfully!'}
            return redirect('main:edit_user_data')
    else:
        print("noooo")
        return render(request, 'main/register.html')
    

    # return render (request=request, template_name="main/register.html", context={"register_form":form})


@csrf_exempt
def login_request(request):
    if request.method == "POST":
        email = request.POST['email_address']
        password = request.POST['password']
        try:
            username = User.objects.get(email=email)
            print("email--", email, "password--", password, "username--", username.email)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                print("user logged in")
                return redirect('/')
            else:
                context = {'error': 'email and password does not match.'}
                return render(request, 'main/login.html', {'context': context})
        except:
            context = {'error': 'user not found go to register'}
            return render(request, 'main/login.html', {'context': context})
    else:
        return render(request, 'main/login.html')


@csrf_exempt
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


@csrf_exempt
def terms_conditions(request):
    if request.method:
        return render(request, 'main/terms_conditions.html')
    else:
        return redirect("/")


"""shipment code """


# API endpoint URL
# Payload with shipping_is_billing set to true
def take_user_data(email):
    # take billing data ffrom user_data table and order data table
    user = user_data.objects.get(email=email)
    user_billing_city = user.city
    user_billing_pincode = user.pincode
    user_billing_state = user.state
    user_billing_email = email
    user_billing_phone = user.phone_number

    # order_user = get_object_or_404(orders, email=email)
    # order_address = order_user.address_1
    # order_total = order_user.order_total
    # order_product = orders.objects.filter(email=email).values_list(order_product)
    order_user = orders.objects.get(email=email)
    print(order_user)
    order_address = order_user.address_1
    order_total = order_user.order_total
    print('11')
    order_product = ast.literal_eval(order_user.products_detail)
    
    print("products", order_product)

    # add value to final order list
    b = final_order_list(email=email, address=order_address, products_detail=order_product, order_total=order_total,
                         shiprocket_dashboard=False)
    final_order_list.save(b)
    print('a1a1')
    order_id = final_order_list.objects.aggregate(Max('order_id'))['order_id__max']
    # order_id =  final_order_list.objects.get(email=email AND adress=order_address)
    
    print("order_id", type(order_id), order_id)

    l2 = []
    # add products  
    print("order_product",order_product,type(order_product))
    for i in order_product:
        print("0000",i)
        name = i.split('-')[0]
        quantity = i.split('-')[1]
        print("name and quantity",name,quantity)
        d1 = {
            "name": name,
            "sku": i,
            "units": quantity,
            "selling_price": "2000",
            "discount": "00",
            "tax": "00",
            "hsn": ""
        }
        l2.append(d1)

    order_data = {
        "order_id": order_id,
        "shipping_is_billing": True,
        "order_date": "2023-08-28 17:17",
        "pickup_location": "Home",
        "channel_id": "",
        "comment": "",
        "reseller_name": "dhruv",
        "company_name": "",
        "billing_customer_name": "dhruv",
        "billing_last_name": "patel",
        "billing_address": order_address,
        "billing_address_2": order_address,
        "billing_isd_code": "",
        "billing_city": user_billing_city,
        "billing_pincode": user_billing_pincode,
        "billing_state": user_billing_state,
        "billing_country": "INDIA",
        "billing_email": user_billing_email,
        "billing_phone": user_billing_phone,
        "billing_alternate_phone": "",
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
        "order_items": l2,
        "payment_method": "prepaid",
        "shipping_charges": "0",
        "giftwrap_charges": "0",
        "transaction_charges": "0",
        "total_discount": "0",
        "sub_total": order_total,
        "length": "10",
        "breadth": "15",
        "height": "20",
        "weight": "1",
        "ewaybill_no": "",
        "customer_gstin": "",
        "invoice_number": "",
        "order_type": ""
    }
    return order_data


def shiprocket_key():
    url = "https://apiv2.shiprocket.in/v1/external/auth/login"
    headers = {
        "Content-Type": "application/json"}
    response = requests.post(url, json={
        "email": "dhruv.180670107033@gmail.com",
        "password": "ShipDhruvRocket@1"}, headers=headers)
    a = response.json()
    return a['token']


def shiprockeet_order_function(request):
    url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"

    # Your API key
    api_key = shiprocket_key()
    # Headers for the request
    headers = {
        "Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    print('aa')
    order_data = take_user_data(email=request.user.email)
    print(order_data)
    # Send the POST request
    response = requests.post(url, json=order_data, headers=headers)

    # Print the response
    print(response.status_code)
    print(response.json())
    return response


"""razor pay code"""
RAZOR_KEY_ID = "rzp_test_PxvxU8NuPVYlN2"
RAZOR_KEY_SECRET = "KP3FhK8rzOJu5Blo3ZvJHBpj"
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))


def homepage(request):
    email = request.user.email
    order_user = orders.objects.get(email=email)
    print(order_user)
    order_address = order_user.address_1
    order_total = order_user.order_total
    order_product = order_user.products_detail

    currency = 'INR'
    amount = order_total * 100  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    # c = user_data.objects.get(email=email)
    # address = str(c.building) +" , "+ str(c.street) + " , " + str(c.area) +" , "+ str(c.pincode) +" , "+ str(c.city)    
    # print(address)
    context['address'] = order_address
    context["order_total"] = order_total
    context["order_product"] = order_product
    return render(request, 'razor_front.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    print("after payment", request.method)
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print("1111111")
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            print(result)
            if result is not None:
                order_user = orders.objects.get(email=request.user.email)
                order_total = order_user.order_total

                amount = order_total * 100  # Rs. 200
                try:
                    print("22222222")
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    print("payment captured")
                    # render success page on successful caputre of payment
                    a = shiprockeet_order_function(request)
                    a
                    print(a.status_code)
                    if a.status_code == 200 and a.json()['status'] == "NEW":
                        order_id = final_order_list.objects.aggregate(Max('order_id'))['order_id__max']
                        order = final_order_list.objects.get(order_id=order_id)
                        order.shiprocket_dashboard = True
                        order.save()
                    else:
                        pass
                    print(a.status_code)
                    print(a.json()['status'])
                    print("ship rocket api is succefully done")
                    return render(request, 'paymentsuccess.html')
                except:
                    print("4444444")
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            print("error")
            return HttpResponseBadRequest()
    else:
        print("method not allowed")
        # if other than POST request is made.
        return HttpResponseBadRequest()
