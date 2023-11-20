from django.db import models
import uuid
from django.contrib.auth.models import User


class VitaminGummies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField(default=True)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/VitaminGummies/")
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="static/images/VitaminGummies/",
                              default='static/images/VitaminGummies/cart.png')

    def clean(self):
        if self.max_quantity <= 0:
            self.stock = False
        elif self.max_quantity >= 1:
            self.stock = True


class EffervescentTablets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField(default=True)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/EffervescentTablets/")
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="static/images/VitaminGummies/",
                              default='static/images/VitaminGummies/cart.png')


class AyurvedicPower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField(default=True)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/AyurvedicPower/")
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="static/images/VitaminGummies/",
                              default='static/images/VitaminGummies/cart.png')


class AyurvedicJuice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField(default=True)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/AyurvedicJuice/")
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="static/images/VitaminGummies/",
                              default='static/images/VitaminGummies/cart.png')


class TropicalSkinHair(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField(default=True)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/TropicalSkinHair/")

    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="static/images/VitaminGummies/",
                              default='static/images/VitaminGummies/cart.png')


class VitaminCapsules(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField(default=True)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/VitaminCapsules/")
    image = models.ImageField(upload_to="static/images/VitaminGummies/",
                              default='static/images/VitaminGummies/cart.png')

    created_on = models.DateTimeField(auto_now_add=True)


class cart_data(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    address_1 = models.CharField(max_length=1000, default="", null=False)
    products_detail = models.JSONField(null=True)
    order_total = models.IntegerField(null=True, default=0)
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
    state = models.CharField(max_length=100, default="GUJARAT")
    phone_number = models.CharField(max_length=100)


class orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    address_1 = models.CharField(max_length=1000, default="INDIA")
    products_detail = models.CharField(max_length=1000, default='empty')
    order_total = models.IntegerField(null=True)


class final_order_list(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    address = models.CharField(max_length=1000, default="INDIA")
    products_detail = models.CharField(max_length=1000, default='empty')
    order_total = models.IntegerField()
    shiprocket_dashboard = models.BooleanField(default=False)


class user_email(models.Model):
    email = models.CharField(max_length=100)
    otp = models.IntegerField()


class subscribed_user(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add=True)


class WishList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.CharField(max_length=50, unique=True)


class PromoCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    discount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=1500)

    def __str__(self):
        return self.code


class PromoCodeVerify(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.code
