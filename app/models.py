from django.db import models
from django.contrib.auth.models import User

class usermodel(User):
    address = models.TextField(default='Enter the correct address')
    phone = models.PositiveBigIntegerField(default="+91 9756897634")

    def __str__(self):
        return f"{self.first_name}{self.last_name}  {self.address}  {self.phone}"

class Products(models.Model):
    product_name = models.CharField(default="Enter Product Name:")
    product_company = models.CharField(default="Enter the Product Brand")
    price = models.FloatField(default="₹100.89")
    quantity = models.CharField(default="Enter Quantity like 200ml,200g..")
    product_details = models.TextField()
    type = models.CharField(default="Enter the type like pouch,can,jar...")
    image = models.ImageField(upload_to='ProductImages/')
    created = models.DateTimeField(auto_now_add=True)

    
    def get_discount(self,product_name,quantity,discount_rate):
        get_model = self.objects.filter(
            product_name=product_name,
            quantity=quantity,
        ).first()
        get_price = get_model.price-((discount_rate/100)*get_model.price) 
        get_model.price = get_price
        get_model.save()
        return f"successfully discount updated for {get_model.product_name} of {get_model.price}"
    
    def __str__(self):
        return f"{self.product_details} {self.price}"

    class Meta:
        models.UniqueConstraint(
            fields=("product_name","product_company","quantity"),name="company and quantity already exists"
        )
        ordering = ["created"]





class UserPurchase(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} {self.product.product_details} {self.product.product_details}"

class Buckets(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    cart = models.PositiveIntegerField()


class PaymentImage(models.Model):
    image = models.ImageField(upload_to='payment')