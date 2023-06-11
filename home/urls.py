from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
   
     path('', views.home, name='home'),
     path('search/', views.search, name='search'),
     path('products/', views.productss, name='products'),
     path('cart/', views.cart, name='cart'),
     path('updatecart/', views.updatecart, name='updatecart'),
     path('tracker/', views.tracker, name='tracker'),
     path('login', views.login, name='login'),
     path('logout', views.logouts, name='logout'),
     path('checkout/', views.checkout, name='checkout'),
     path('processorder/', views.processorder, name='processorder'),
     path('signin', views.signin, name='signin'),
     path('user/', views.user, name='user'),
     path('contact', views.Contact, name='contact'),
     path('single/BookOrder',views.singleproduct,name ='singleproduct'),
     path('check/', views.check, name='check'),
     path('UserLogin', views.UserLogin, name="UserLogin"),
      path('Signup', views.Signup, name="Signup"),
      path('BookOrder', views.BookOrder, name="BookOrder"),
       path('AddProductAction', views.AddProductAction, name="AddProductAction"),
        path('ViewOrders', views.ViewOrders, name="ViewOrders"),
        path('viewproducts', views.viewproducts, name="viewproducts"),
]