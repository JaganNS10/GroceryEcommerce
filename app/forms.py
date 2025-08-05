from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Products,usermodel

class RegisterUser(UserCreationForm):

    class Meta:

        model = usermodel

        fields = ["username","first_name","last_name","email","address","phone","password1","password2"]


class AddProducts(forms.ModelForm):

    class Meta:

        model = Products
        fields = "__all__"



class Edit(forms.ModelForm):

    class Meta:

        model = usermodel

        fields = ["address","email","phone"]



class Change_Password(forms.Form):

    otp_field = forms.CharField(max_length=6,help_text='Enter Your OTP:',required=True)


class PasswordFields(forms.Form):

    password1 = forms.CharField(required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(),required=True)


    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1!=password2:
            raise forms.ValidationError("Oops! the password fields does not match.please check two password fields :)")
        else:
            return super().clean()
        # print(self.cleaned_data)
        # print(super().clean())



class OnlinePayment(forms.Form):

    recipt=forms.ImageField()




