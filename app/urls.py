from . import views
from django.urls import path,include



urlpatterns = [
    path("Home/",views.Home,name='Home'),
    path("AddProducturl/",views.AddProductView,name='AddProducturl'),
    path("GetProduct/",views.GetProduct,name='GetProduct'),
    path("GetProduct/<value>/",views.GetProduct,name='GetProduct'),
    path("ViewProduct/<int:pk>/",views.ViewProduct,name='ViewProduct'),
    path('ViewCart/',views.ViewCart,name='ViewCart'),
    path('addCart/<int:pk>',views.addCart,name='ViewCart'),
    path('IncrementProduct/<int:pk>/',views.IncrementProduct,name='IncrementProduct'),
    path("DecrementProduct/<int:pk>/",views.DecrementProduct,name='DecrementProduct'),
    path('Register/',views.RegisterView,name='Register'),
    path('Login/',views.Login,name='Login'),
    path("Logout/",views.Logout,name='Logout'),
    path("filter/",views.filter,name='filter'),
    path('payment/',views.payment,name='payment'),
    path('editprofile/<int:pk>/',views.EditProfile,name='editprofile'),
    path('profile/',views.profile,name='profile'),
    path('confirm_cash/',views.confirm_cash,name='Cash'),
    path('cash/',views.Cash,name='Cash'),
    path('orders/',views.Myorders,name='orders'),
    path('changepassword/',views.ChangePassword,name='changepassword'),
    path('password/',views.password,name='password'),
    path('Online/',views.Online_Payment,name='Online')
]