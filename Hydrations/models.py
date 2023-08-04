from django.db import models


class VitaminGummies(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/VitaminGummies/")
    created_on = models.DateTimeField(auto_now_add=True)


class EffervescentTablets(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/EffervescentTablets/")
    created_on = models.DateTimeField(auto_now_add=True)


class AyurvedicPower(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/AyurvedicPower/")
    created_on = models.DateTimeField(auto_now_add=True)


class AyurvedicJuice(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/AyurvedicJuice/")
    created_on = models.DateTimeField(auto_now_add=True)


class TropicalSkinHair(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/TropicalSkinHair/")
    created_on = models.DateTimeField(auto_now_add=True)


class VitaminCapsules(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField()
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/VitaminCapsules/")
    created_on = models.DateTimeField(auto_now_add=True)