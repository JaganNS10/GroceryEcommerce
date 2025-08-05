from .forms import RegisterUser,AddProducts,Edit,Change_Password,PasswordFields,OnlinePaymentform
from .models import Products,usermodel,Buckets,UserPurchase,PaymentImage


from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client
import random
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
from PIL import Image
import datetime
from django.db.models import Q
import os
import requests



def Home(request):
    
    if request.user.is_authenticated:
        GetCart = CartDetails(request)
        List = GetCart[1]
        link = '/rooturl/profile/'
        
        return render(
            request,
            "index.html",
            {"count":List[0],"name":"Profile","link":link,"Name":"Orders","logo":"briefcase-outline","Link":"/rooturl/orders/"}
        )
    else:
        link = '/rooturl/Register/'
        return render(request,"index.html",{"count":0,"name":"Register","link":link,"Name":"Login","logo":"person-add-outline","Link":"/rooturl/Login"})

#@login_required(login_url='Home')
def AddProductView(request):
    if request.method == "POST":
        form = AddProducts(request.POST,files=request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            messages.success(request,f"product saved {data.get('product_details')}")
            # return redirect('Home')
        else:
            messages.error(request,form.errors)
    else:
        form = AddProducts()
    GetCart = CartDetails(request)
    # List = GetCart[1]"count":List[0]
    link = '/rooturl/profile/'
  
    return render(
        request,
        'AddProduct.html',

        {"form":form,"name":"profile","link":link,"Name":"Orders","logo":"briefcase-outline","Link":"/rooturl/orders/"}
    )

name = []
@login_required(login_url='Login')
def GetProduct(request,value=None):
        if value is None:
            instance = name
        else:
            instance = Products.objects.filter(product_name=value)
            if not instance:
                messages.error(request,'Sorry,Your Product was not found.')
                return redirect("Home")
            
        product_name = []
        Type = []
        for i in instance:
            if i.product_company not in product_name:
                product_name.append(i.product_company)
            if i.type not in Type:
                Type.append(i.type)
        GetCart = CartDetails(request)
        List = GetCart[1]
        link = '/rooturl/profile/'
        
        return render(request,"GetProduct.html",{'data':instance,"product_name":product_name,"Type":Type,"count":List[0],"name":"profile","link":link,"Name":"Orders","logo":"briefcase-outline","Link":"/rooturl/orders/"})

@login_required(login_url='Login')
def ViewProduct(request,pk):
    instance = Products.objects.get(id=pk)
    del_price = instance.price+20
    GetCart = CartDetails(request)
    Cart = GetCart[0]
    List = GetCart[1]
    link = '/rooturl/profile/'
    
    return render(request,'ViewProduct.html',{"data":instance,"del":del_price,"count":List[0],"name":"profile","link":link,"Name":"Orders","logo":"briefcase-outline","Link":"/rooturl/orders/"})

@login_required(login_url='Login')
def addCart(request,pk):
    instance = Products.objects.get(id=pk)
    user = usermodel.objects.get(id=request.user.id)
    get = Buckets.objects.filter(user=user,product=instance)
    print(get)
    if not get:
        Buckets.objects.create(user=user,product=instance,cart=1)
    elif instance:
        increment = get.first()
        increment.cart+=1
        increment.save()
    messages.success(request,f"{instance.product_details} Added to Cart.")
    return HttpResponseRedirect(f'/rooturl/GetProduct/{instance.product_name}')

# Create your views here.

@login_required(login_url='Login')
def IncrementProduct(request,pk):
    get_buck = Buckets.objects.get(id=pk)
    if get_buck.cart>0:
        get_buck.cart+=1
        get_buck.save()
    print("increment:",get_buck.cart)
    return HttpResponseRedirect("/rooturl/ViewCart/")
@login_required(login_url='Login')
def DecrementProduct(request,pk):
    get_buck = Buckets.objects.get(id=pk)
    if get_buck.cart!=1:
        get_buck.cart-=1
        get_buck.save()
    else:
        get_buck.delete()
    
    return redirect("ViewCart")

@login_required(login_url='Login')
def ViewCart(request):
    GetCart = CartDetails(request)
    Cart = GetCart[0]
    List = GetCart[1]
    #price
    get_price = Price(Cart)
    price = get_price[0]
    total = get_price[1]
    link = '/rooturl/profile/'
   
    return render(request,'Cart.html',{"Cart":Cart,"count":List[0],"price":price[0],"total":total,"name":"profile","link":link,"Name":"Orders","logo":"briefcase-outline","Link":"/rooturl/orders/"})

@login_required(login_url='Login')
def filter(request):
    if request.method == "POST":
        print(request.POST)
        value = request.POST['search']
        items = Products.objects.all()
        n = []
        for i in items:
            if i.product_name in value.replace(" ","").lower() or value.replace(" ","").lower() in i.product_details.replace(" ","").lower():
                n.append(i)

        if n:
            name.clear()
            name.extend(n)
            return HttpResponseRedirect(f"/rooturl/GetProduct/")
        else:
            messages.error(request,'oops! your product not found.pls search correctly...')
            return redirect("Home")

@login_required(login_url='Login')
def payment(request):
    GetCart = CartDetails(request)
    if GetCart[1][0] != 0:
        GetPrice = Price(GetCart[0])
        price = GetPrice[0]
        total = GetPrice[1]
        user  = usermodel.objects.get(id=request.user.id)
        link = '/rooturl/profile/'
        
        return render(request,'payment.html',{'price':price[0],'total':total,"count":GetCart[1][0],"user":user,"name":"profile","link":link,"Name":"Orders","logo":"briefcase-outline","Link":"/rooturl/orders/"})
    else:
        messages.error(request,'Your Cart is empty.You have to buy something to continue.')
        return redirect('Home')
    
def confirm_cash(request):
    GetCart = CartDetails(request)
    List = GetCart[1]
    link = '/rooturl/profile/'
    return render(request,'cash.html',{"count":List[0],"name":"profile","link":link,"Name":"Orders","logo":"briefcase-outline","Link":"/rooturl/orders/"})


pay = ["Cash On Delivery"]

@login_required(login_url='Login')
def Cash(request):
    GetCart = CartDetails(request)
    price = Price(GetCart[0])
         
    product = []
    for i in GetCart[0]:
            item = i.product.product_details+" "+"-"+" "+str(i.cart)
            product.append(item)
        
    
    number = random.randrange(10000000000000000,10000000000000000000)
        
    otp = random.randrange(100000,900000)
    order_id = "ORID"+str(number)

    subject = f"Regarding Grocery-Shop.Your OrderID: {order_id}"
    message = f"Hi {request.user} from Grocery-Shop Ecommerce.\nYour Order {",".join(product)} has been Placed Succesfully.\nYour items price is {price[1]}. OTP {otp}\nYour Order delivered within the day.Continue Shopping:)"
    send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [request.user.email]
    )


    #send message to admin
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    number_list = ["+91 7904136090"]
    client = Client(account_sid,auth_token)
    get = usermodel.objects.get(id=request.user.id)
    request.session['payment'] = ['cash on delivery']
    details = f"Name: {get.first_name} {get.last_login}\n Phone No: {get.phone}\nAddress: {get.address}\nOtp:  {otp}\nOrderId:  {order_id}\nProducts: {",".join(product)}\nPrice: {price[1]}\nPayment: {request.session['payment']}"
    for r in number_list:
        msg = client.messages.create(
            body= f"{details}",
            from_= "+18152474413",
            to=r
        )
    
    #adduser purchase
    for j in GetCart[0]:
        UserPurchase.objects.create(user=j.user,product=j.product)
    
    #remove bucket
    for k in GetCart[0]:
        k.delete()

    messages.success(request,'Your Order has been places')
    return redirect('Home')
       

login_required(login_url='Login')
def Myorders(request):
    user = UserPurchase.objects.filter(user=request.user)
    GetCart = CartDetails(request)
    List = GetCart[1]
    link = '/rooturl/profile/'
    return render(request,'orders.html',{"user":user,"count":List[0],"name":"Profile","link":link,"Name":"Orders","logo":"briefcase-outline"})

@login_required(login_url='Login')
def ChangePassword(request):
    if request.method == "POST":
        form = Change_Password(request.POST)
        print(request.session['otp'])
        if form.is_valid():
            user_otp = form.cleaned_data.get('otp_field')
            if str(request.session['otp']) == user_otp:
                messages.success(request,'Your OTP is valid.Now Your change the password.')
                return redirect('password')
            else:
                print(False)
                messages.error(request,'Enter Correct Otp....')
    else:
        otp = random.randint(100000,1000000)
        send_mail(
            f"Regarding Password Change for User {request.user} From Grocery-Shop",
            f"Your Otp is :{otp}",
            settings.EMAIL_HOST_USER,
            [request.user.email]
        )
        request.session["otp"] = otp
        print(request.session['otp'])
        messages.success(request,'otp send successfully to registed email...')

    form = Change_Password()
    return render(request,"changepassword.html",{"form":form})

@login_required(login_url='Login')
def password(request):
    if request.method == "POST":
        form = PasswordFields(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = usermodel.objects.get(id=request.user.id)
            user.set_password(data.get('password2'))
            user.save()
            messages.success(request,'Your Password Changed Succesfully')
            return redirect('Login')
        else:
            print(form.errors)
            messages.error(request,"Oops! the password fields does not match.please check two password fields :)")
    form = PasswordFields()
    return render(request,'password.html',{"form":form})


@login_required(login_url='Login')
# def Online_Payment(request):
#     GetCart = CartDetails(request)
#     List = GetCart[1]
#     link = '/rooturl/profile/'
#     GetPrice = Price(GetCart[0])
#     total = GetPrice[1]

#     date = datetime.date.today()
#     month = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
#     day = str(date.day)
#     monthmap = month[date.month]
#     year = str(date.year)
#     print(day,monthmap,year)



#     if request.method == "POST":
#         form = OnlinePaymentform(request.POST,request.FILES)
#         if form.is_valid():
#             data = request.FILES['recipt']
#             save_image = PaymentImage.objects.create(image=data)
#             image = save_image.image.file
#             open_image = Image.open(data)
#             gpay_id = "Google Pay + jagan1Ons@oksbi"
#             change_image_text = pytesseract.image_to_string(open_image)
#             # print(change_image_text,total)
#             if ("Completed" in change_image_text) and (str(int(total)) in change_image_text) and (day in change_image_text and monthmap in change_image_text and year in change_image_text) and ("To: JOTHILAKSHMI S" in change_image_text):
#                 print(True)
#                 request.session['payment'] = 'Online Payment'
#                 return redirect('Cash')
#             else:
#                 save_image.image.delete()
#                 save_image.delete()
#                 messages.error(request,'Oops! You are uploaded Wrong recipt!')
#     else:
#         form = OnlinePaymentform()
#     return render(request,'Online.html',{"form":form,"count":List[0],"name":"Profile","link":link,"Name":"Orders","logo":"briefcase-outline"}) 



def extract_text_from_image(image_file):
    api_key = 'K83656049788957'  # 🔁 Replace this with your real OCR.Space API key
    url = 'https://api.ocr.space/parse/image'

    response = requests.post(
        url,
        files={'filename': image_file},
        data={'apikey': api_key, 'language': 'eng'}
    )

    try:
        result_json = response.json()
        return result_json["ParsedResults"][0]["ParsedText"]
    except (KeyError, IndexError):
        return ""
    
def Online_Payment(request):
    try:
        GetCart = CartDetails(request)
        List = GetCart[1]
        link = '/rooturl/profile/'
        GetPrice = Price(GetCart[0])
        total = GetPrice[1]

        date = datetime.date.today()
        month = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        day = str(date.day)
        monthmap = month[date.month]
        year = str(date.year)

        if request.method == "POST":
            form = OnlinePaymentform(request.POST, request.FILES)
            if form.is_valid():
                if 'recipt' not in request.FILES:
                    messages.error(request, "Receipt not uploaded!")
                    return redirect(request.path)
                
                data = request.FILES['recipt']
                save_image = PaymentImage.objects.create(image=data)

                try:
                    extracted_text = extract_text_from_image(data)
                except Exception as e:
                    print("OCR error:", e)
                    save_image.delete()
                    messages.error(request, "Unable to read the receipt image.")
                    return redirect(request.path)

                if (
                    "Completed" in extracted_text and
                    str(int(total)) in extracted_text and
                    day in extracted_text and
                    monthmap in extracted_text  and
                    year in extracted_text and
                    "To: JOTHILAKSHMI S" in extracted_text 
                ):
                    request.session['payment'] = 'Online Payment'
                    return redirect('Cash')
                else:
                    save_image.image.delete()
                    save_image.delete()
                    messages.error(request, 'Oops! You uploaded the wrong receipt!')
        else:
            form = OnlinePaymentform()

        return render(request, 'Online.html', {
            "form": form,
            "count": List[0],
            "name": "Profile",
            "link": link,
            "Name": "Orders",
            "logo": "briefcase-outline"
        })

    except Exception as e:
        import traceback
        print("Error in Online_Payment:", e)
        traceback.print_exc()
        return render(request, 'error.html', {"message": "Something went wrong in Online Payment."})


def Price(Cart):
    price = [1]
    if Cart:
        for i in Cart:
            price_items = i.product.price
            amount = i.cart
            price[0] = price[0]+(price_items*amount)
    price[0] = price[0]-1
    total = price[0]+9+39
    return [price,total]

@login_required(login_url='Login')
def CartDetails(request):
    List = [0]
    Cart = []


    get = Buckets.objects.filter(user=request.user)
    if get:
        for i in get:
            if i not in Cart:
                Cart.append(i)
        List[0] = len(list(get)) 
        print(List,Cart)
        return [Cart,List]
    return [Cart,List]


@login_required(login_url='Login')
def profile(request):
    GetCart = CartDetails(request)
    List = GetCart[1]
    user = usermodel.objects.get(id=request.user.id)
    return render(request,'profile.html',{'user':user,"count":List[0],"name":"profile","Name":"Orders","logo":"briefcase-outline","Link":"/rooturl/orders/"})

@login_required(login_url='Login')
def EditProfile(request,pk):
    get = usermodel.objects.get(id=pk)
    if request.method == "POST":
        form = Edit(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            get.address = data.get('address')
            get.phone = data.get('phone')
            get.email = data.get('email')
            get.save()
            messages.success(request,'Your Profile Updated Successfully...')
            return redirect('payment')

        else:
            messages.error(request,form.errors)
    form = Edit(instance=get)
    return render(request,'editprofile.html',{"form":form})


def RegisterView(request):
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"Register Successfully {request.POST['username']}")
            return redirect('Login')
        else:
            messages.error(request,form.errors)
            form = RegisterUser(request.POST)
    else:
        form = RegisterUser()
    return render(request,'Register.html',{"form":form})

def Login(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,f'{user.username} successfully login')
            return redirect('Home')
        else:
            messages.error(request,form.errors)
            print(form.errors)
    form = AuthenticationForm()
    return render(request,'login.html',{"form":form})




def Logout(request):
    logout(request)
    return redirect('Home')





