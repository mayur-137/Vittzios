from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import CreateView
from .forms import ContactFormModel
from .models import VitaminGummies, EffervescentTablets, AyurvedicPower, ContactModel ,user_data
from django.shortcuts import  render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login, authenticate, logout #add this
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactFormModel,NewUserForm
from django.contrib.auth.models import User,auth



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
        print(self.request.POST.get('email'))
        print(form['name'].value())

        print(form.cleaned_data['name'])
        print(form.cleaned_data['email'])
        print(form.cleaned_data['message'])

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
         
            
# def user_data(request):
#   print(request.method)
#             email = email
#             building = request.POST['building']
#             street = request.POST['street']    
#             area = request.POST['area']
#             pincode = request.POST['pincode']
#             city = request.POST['city']
#             user = user_data.objects.create_user(email=email,building=building,street=street,area=area,pincode=pincode,city=city)
#             print("user data is ready to store")
#             user.save()
#             print("user data stored")
#             return redirect('/') 
       
@csrf_exempt
def register_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            print("user already registered")
            context = {'error': 'The username you entered has already been taken. Please try another username.'}
            return render(request, 'main/register.html', {'context': context})
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
	return redirect("main:homepage")

# @csrf_exempt
# def user_data(request):
#     if request.method == "POST":
#         email = request.user.email
#         print(email)            
#         # return render(request ,'main/user_data.html' , {'context': context})
#     else:
#         return render(request,'main/user_data.html')


