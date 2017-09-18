from django.conf.urls import url
from product_manage import views

urlpatterns = [
    url(r'^list_(\d+)_(\d+)_(\d+)/$', views.list_products),
    url(r'^(\d+)$', views.detail),
]