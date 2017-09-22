from django.conf.urls import url
from cart_manage import views

urlpatterns = [
    url(r'', views.view_cart, name="cart"),
    url(r'^add/(?P<product_id>\d+)', views.add_to_cart, name="add_product_to_cart"),
    url(r'^clean', views.clean_cart, name="clean_cart"),
]
