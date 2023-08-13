from django.contrib import admin
from .models import VitaminGummies, EffervescentTablets, VitaminCapsules, AyurvedicJuice, AyurvedicPower, \
    TropicalSkinHair, CartModel, ContactModel, ProductBuyDetails


# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "price", "discount", "slug", "quantity", "picture",
                    "created_on"]


admin.site.register(VitaminGummies, AuthorAdmin)
admin.site.register(EffervescentTablets, AuthorAdmin)
admin.site.register(VitaminCapsules, AuthorAdmin)
admin.site.register(AyurvedicPower, AuthorAdmin)
admin.site.register(AyurvedicJuice, AuthorAdmin)
admin.site.register(TropicalSkinHair, AuthorAdmin)
admin.site.register(CartModel, AuthorAdmin)


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "created_on"]


@admin.register(ProductBuyDetails)
class ProductBuyDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "slug"]
