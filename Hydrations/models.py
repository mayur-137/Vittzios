from django.db import models
import uuid


class VitaminGummies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/VitaminGummies/")
    created_on = models.DateTimeField(auto_now_add=True)


class EffervescentTablets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/EffervescentTablets/")
    created_on = models.DateTimeField(auto_now_add=True)


class AyurvedicPower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/AyurvedicPower/")
    created_on = models.DateTimeField(auto_now_add=True)


class AyurvedicJuice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/AyurvedicJuice/")
    created_on = models.DateTimeField(auto_now_add=True)


class TropicalSkinHair(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/TropicalSkinHair/")
    created_on = models.DateTimeField(auto_now_add=True)


class VitaminCapsules(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/VitaminCapsules/")
    created_on = models.DateTimeField(auto_now_add=True)


class CartModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/CartModules/")
    created_on = models.DateTimeField(auto_now_add=True)


class ContactModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    message = models.TextField(max_length=4000)
    created_on = models.DateTimeField(auto_now_add=True)

class user_data(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100)
    building = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,default="GUJRAT")
    phone_number = models.CharField(max_length=100)


class orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    address_1 = models.CharField(max_length=1000,default="INDIA")
    # product_picture = models.ImageField(upload_to="static/images/VitaminCapsules/",default="")
    products_detail = models.CharField(max_length=1000,default='empty')
    order_total = models.IntegerField()

class final_order_list(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    address = models.CharField(max_length=1000,default="INDIA")
    products_detail = models.CharField(max_length=1000,default='empty')
    order_total = models.IntegerField()
    shiprocket_dashboard = models.BooleanField(default=False)    

    
# class ProductBuyDetails(models.Model):
#     pass
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # email = models.EmailField()
    # slug = models.SlugField(unique=True, max_length=255)