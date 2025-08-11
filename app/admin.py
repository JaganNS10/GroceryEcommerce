from django.contrib import admin
from . import models




admin.site.register(models.usermodel)
admin.site.register(models.Products)
admin.site.register(models.UserPurchase)
admin.site.register(models.Buckets)
admin.site.register(models.PaymentImage)
# Register your models here.
