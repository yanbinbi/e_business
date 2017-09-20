from django.conf.urls import url
from product_manage import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list_(\d+)_(\d+)_(\d+)/$', views.list_products),
    url(r'^(?P<product_id>\d+)$', views.detail, name="detail"),
]