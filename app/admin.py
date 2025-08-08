from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_name","product_company","price","quantity"]

class usermodelAdmin(admin.ModelAdmin):
    list_display = ["first_name","last_name","address","phone"]

class BucketsAdmin(admin.ModelAdmin):
    list_display = ["user","product","cart"]

admin.site.register(models.usermodel,usermodelAdmin)
admin.site.register(models.Products,ProductAdmin)
admin.site.register(models.UserPurchase)
admin.site.register(models.Buckets,BucketsAdmin)
admin.site.register(models.PaymentImage)
# Register your models here.
