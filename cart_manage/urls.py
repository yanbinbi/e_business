from django.conf.urls import url
from cart_manage import views

urlpatterns = [
    url(r'', views.cart, name="cart"),
]