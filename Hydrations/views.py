from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views import View
from .forms import ContactFormModel
from .models import VitaminGummies, EffervescentTablets, AyurvedicPower, ContactModel ,user_data
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login, authenticate, logout #add this
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactFormModel,NewUserForm
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseBadRequest, Http404
from razorpay import Client
import razorpay
from django.views.decorators.csrf import csrf_exempt



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
            except Http404:
                pass
        cart_session = request.session.get('cart_session', {})
        cart_session[product_id] = cart_session.get(product_id, 0) + 1
        request.session['cart_session'] = cart_session
        print(request.session['cart_session'], "1")
        print(cart_session, "2")
        return redirect("/cart/")
    

class CartView(View):

    def get(self, request, *args, **kwargs):
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
                # print(cart.keys(), "4")
                # print(itm, model, "itm")
                if itm:
                    products_in_cart.append(itm)
                    # print(model, "i am in if")
                # products_in_cart.append(itm)
                # print(products_in_cart, "5")
                # products_in_cart.clear()
            except:
                pass
        for products in products_in_cart:
            # print(products, "products ")
            # print(products_in_cart, "cart==================")
            for product in products:
                # print(product, "6")
                # print(product.price, "price")
                # print(cart[str(product.id)], "quntity")
                product.subtotal = product.price * cart[str(product.id)]
                # print(product.subtotal, "subtotal")
                product_total = product.subtotal + product_total
                # print(product_total, "total")
                product.product_quantity = str(cart[str(product.id)])
                # print(str(cart[str(product.id)]), "str(cart[str(product.id)])")
                products_list.append(product)
            # print(products_list, "list")
        return render(request, 'cart.html', {'products': products_list, 'product_total': product_total})


class Update_cart_view(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.GetMaxQuantity = None

    def post(self, request, *args, **kwargs):
        Product_id = request.POST.get("Update_product_quantity")
        print(Product_id, "ID")
        Mode_of_Operations = request.POST.get("minus")
        if Mode_of_Operations == "-":
            cart_session = request.session.get('cart_session', {})
            cart_session[Product_id] = cart_session.get(Product_id) - 1
            request.session['cart_session'] = cart_session
            if cart_session.get(Product_id) == 0:
                del cart_session[Product_id]
        else:
            models = [VitaminGummies, EffervescentTablets, AyurvedicPower]
            for model in models:
                try:
                    self.GetMaxQuantity = model.objects.filter(id=Product_id).values("max_quantity").get()
                except:
                    pass
            cart_session = request.session.get('cart_session', {})
            if not cart_session.get(Product_id) == self.GetMaxQuantity["max_quantity"]:
                cart_session[Product_id] = cart_session.get(Product_id) + 1
                request.session['cart_session'] = cart_session
        return redirect("/cart/")
    
class RemoveItemView(View):

    def post(self, request, *args, **kwargs):
        GetRemoveItemId = request.POST.get("removeItem")
        cart_session = request.session.get('cart_session', {})
        models = [VitaminGummies, EffervescentTablets, AyurvedicPower]
        for model in models:
            try:
                product = get_object_or_404(model, id=GetRemoveItemId)
            except Http404:
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
            context = {"email":email,"phone_number":phone_number,'username':username,'building':building,'street':street,'area':area,'pincode':pincode,'city':city}
            print(context)
            return render(request,'main/user_data.html' ,{'context': context})
                
        except:
            return render(request,'main/user_data.html')
    else:       
        return render(request, 'main/user_data.html')


def edit_user_data(request):
    print("edit user data")
    if request.method =="POST":
        print("edit user data222")
        current_user = request.user
        email = current_user.email 
        building = request.POST['building'] 
        street = request.POST['street']     
        area = request.POST['area'] 
        pincode = request.POST['pincode'] 
        city = request.POST['city'] 
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
            user.save()
        else: 
            print("user data is not saved")
            b = user_data(email=email,building=building,street=street,area=area,pincode=pincode,city=city,phone_number=phone_number)
            user_data.save(b)
        return redirect('/')
    else:
        return render(request,'main/edit_user_data.html')

        
@csrf_exempt
def register_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        print(username,email,password)
        if User.objects.filter(username=username).exists():
            print("user already registered")
            context = {'error': 'The username you entered has already been taken. Please try another username.'}
            return render(request, 'main/register.html', {'context': context})
        elif User.objects.filter(email=email).exists():
            print("this email is already taken try another one")
            context = {"error":"this email is already taken try another one"}
            return render(request , 'main/register.html',{"context":context})
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            print("user created")
            # context = {'error': 'User registered successfully!'}
            return redirect('main:login')
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
            print("email--",email,"password--",password,"username--",username.email)
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                print("user logged in")
                return redirect('/')
            else:
                context = {'error': 'email and password does not match.'}
                return render(request, 'main/login.html', {'context': context})
        except:
                context = {'error': 'user not found go to register' }
                return render(request, 'main/login.html', {'context': context})            
    else:
        return render(request,'main/login.html')

@csrf_exempt
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")


@csrf_exempt
def terms_conditions(request):
    if request.method:
        return render(request,'main/terms_conditions.html')
    else:
        return redirect("/")

@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        print(request,"****************************")

        markup = requests.get("http://127.0.0.1:8000/male/")
        soup = BeautifulSoup(markup.content,'html.parser')
        # print([x for x in soup.find_all('div',attrs={"class":'destination_title'})],'@@@@@@@@@@')

        product_name = soup.find('a', id="name")
        product_price = soup.find('div', id="price")
        product_desc = soup.find('div', id="desc")
        product_image = soup.find('div', id="image")


        cart_data = cart_items( pro_name=product_name.string,pro_price=product_price.string[7:],
                                pro_desc=product_desc.string)
        cart_data.save()

        return redirect('/')

# def initiate_payment(request):
#     if request.method == "post":

#         # Extract the necessary data from the request
#         amount = 1000  # Example amount in paise (INR)
        
#         # Initialize the Razorpay client
#         razorpay_client = Client(auth=("your_key_id", "your_key_secret"))
#         print("ready to payment")
#         # Create a Razorpay order
#         order = razorpay_client.order.create(data={
#             "amount": amount,
#             "currency": "INR",
#             # Add other order details if required
#         })

#         return JsonResponse(order)  # Return the order details to the frontend
#     else:
#         return render(request,'razor_front.html')

"""shipment code """
import requests

# API endpoint URL
# Payload with shipping_is_billing set to true
order_data = {
        "order_id": "6",
        "shipping_is_billing": True,
        "order_date": "2023-08-28 17:17",
        "pickup_location": "Home",
        "channel_id": "",
        "comment": "",
        "reseller_name": "dhruv",
        "company_name": "",
        "billing_customer_name": "dhruv",
        "billing_last_name": "patel",
        "billing_address": "10 nilmali aprtment , gurukul road , ahmedabad",
        "billing_address_2": "near sant.ans school",
        "billing_isd_code": "",
        "billing_city": "ahemdabad",
        "billing_pincode": "380015",
        "billing_state": "gujrat",
        "billing_country": "INDIA",
        "billing_email": "dhruv.ladola@appuni.com",
        "billing_phone": "9033474857",
        "billing_alternate_phone":"",
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
        "order_items": [
            {
                "name": "t-shirt",
                "sku": "chakra123",
                "units": "1",
                "selling_price": "2000",
                "discount": "00",
                "tax": "00",
                "hsn": ""
            }
        ],
        "payment_method": "prepaid",
        "shipping_charges": "0",
        "giftwrap_charges": "0",
        "transaction_charges": "0",
        "total_discount": "0",
        "sub_total": "2000",
        "length": "10",
        "breadth": "15",
        "height": "20",
        "weight": "1",
        "ewaybill_no": "",
        "customer_gstin": "",
        "invoice_number":"",
        "order_type":""
    }

def shiprockeet_order_function(order_data):
    url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"

    # Your API key
    api_key =  'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaXYyLnNoaXByb2NrZXQuaW4vdjEvZXh0ZXJuYWwvYXV0aC9sb2dpbiIsImlhdCI6MTY5MzIyMDMyNCwiZXhwIjoxNjk0MDg0MzI0LCJuYmYiOjE2OTMyMjAzMjQsImp0aSI6IjZZemhJTlBLVjNLaVUzSGwiLCJzdWIiOjM4NTM3MTEsInBydiI6IjA1YmI2NjBmNjdjYWM3NDVmN2IzZGExZWVmMTk3MTk1YTIxMWU2ZDkifQ.XylRNgyjbssnb4JH_nz7mFRai3gFgJW2sNKEtyzIRSo'

    # Headers for the request
    headers = {
        "Content-Type": "application/json","Authorization": f"Bearer {api_key}"}
    
    # Send the POST request
    response = requests.post(url, json=order_data, headers=headers)

    # Print the response
    print(response.status_code)
    print(response.json())


"""razor pay code"""
RAZOR_KEY_ID = "rzp_test_PxvxU8NuPVYlN2"
RAZOR_KEY_SECRET = "KP3FhK8rzOJu5Blo3ZvJHBpj"
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def homepage(request):
    currency = 'INR'
    amount = 20000  # Rs. 200
 
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
 
    return render(request, 'razor_front.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    print("after payment",request.method)
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
                amount = 20000  # Rs. 200
                try:
                    print("22222222")
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    shiprockeet_order_function(order_data)
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

