"""webshop URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from webshop_app.views import \
    HomeView, \
    LoginView, \
    RegistrationView, \
    LogoutView, \
    LoggedView, \
    CpuView, \
    GpuView, \
    MotherboardView, \
    ProductView, \
    AddressView, \
    UpdateUserView, \
    ChangePasswordView, \
    AddAddressView, \
    ChangeAddressView, \
    CartView, \
    OrderView, \
    add_to_cart, \
    remove_from_cart, \
    remove_comment


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="base"),
    path('home/', HomeView.as_view(), name="home"),
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('updateuser/', UpdateUserView.as_view(), name="update-user"),
    path('changepassword/', ChangePasswordView.as_view(), name="change-password"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('logged/', LoggedView.as_view(), name="logged"),
    path('address/<int:address_id>/', AddressView.as_view(), name="address"),
    path('addaddress/', AddAddressView.as_view(), name="add-address"),
    path('changeaddress/<int:address_id>/', ChangeAddressView.as_view(), name="change-address"),
    path('cart/', CartView.as_view(), name="cart"),
    path('add-to-cart/<pk>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<cart_id>/', remove_from_cart, name="remove-from-cart"),
    path('order/<order_id>/', OrderView.as_view(), name="order"),
    path('category/cpu/', CpuView.as_view(), name="category-cpu"),
    path('category/gpu/', GpuView.as_view(), name="category-gpu"),
    path('category/motherboards/', MotherboardView.as_view(), name="category-motherboard"),
    path('product/<int:pk>/', ProductView.as_view(), name="product"),
    path('remove-comment/<comment_id>/<pk>/', remove_comment, name="remove-comment"),
]
