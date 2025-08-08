from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings

# models.py
class usermodel(AbstractUser):
    address = models.TextField(help_text='Enter the correct address')
    phone = models.CharField(max_length=10, help_text='9756897634')


    def __str__(self):
        return f"{self.first_name}{self.last_name}  {self.address}  {self.phone}"

class Products(models.Model):
    product_name = models.CharField(help_text="Enter Product Name:")
    product_company = models.CharField(help_text="Enter the Product Brand")
    price = models.FloatField(help_text="₹100.89")
    quantity = models.CharField(help_text="Enter Quantity like 200ml,200g..")
    product_details = models.TextField()
    type = models.CharField(help_text="Enter the type like pouch,can,jar...")
    image = models.ImageField(upload_to='ProductImages/',null=True)
    url = models.URLField()
    discount = models.IntegerField(help_text="Add discount.Not mandantory.You Can leave this field.",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.product_details} {self.price}"

    class Meta:
        models.UniqueConstraint(
            fields=("product_name","product_company","quantity"),name="company and quantity already exists"
        )
        ordering = ["created"]





class UserPurchase(models.Model):
    user = models.ForeignKey(usermodel,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} {self.product.product_details} {self.product.product_details}"

class Buckets(models.Model):
    user = models.ForeignKey(usermodel,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    cart = models.PositiveIntegerField()


class PaymentImage(models.Model):
    image = models.ImageField(upload_to='payment')