from django.contrib import admin
from .models import VitaminGummies, EffervescentTablets, VitaminCapsules, AyurvedicJuice, AyurvedicPower, \
    TropicalSkinHair, CartModel, ContactModel , user_data ,orders


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "email","building","street","street",'area','pincode' ,'city']
    
admin.site.register(user_data,AuthorAdmin)    

class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "price", "discount", "slug", "max_quantity", "picture",
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

class AuthorAdmin_order(admin.ModelAdmin):
    list_display = ["email","address_1","products_detail","order_total"]
admin.site.register(orders,AuthorAdmin_order)

# @admin.register(ProductBuyDetails)
# class ProductBuyDetailsAdmin(admin.ModelAdmin):
#     list_display = ["id", "slug"]