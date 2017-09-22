from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from cart_manage.models import Cart, LineItem
from product_manage.models import Product
from cart_manage.forms import ProductAddToCartForm
import json


# Create your views here.
def view_cart(request):
    try:
        # 试图获取session中的购物车
        carts = request.session.get("carts", None)
        t = get_template('cart_manage/shopcart.html')
        # 如果session中没有购物车对象，则新创建一个并且把它加到session中
        if not carts:
            carts = Cart()
            request.session["carts"] = carts

        context = {
            "carts": carts,
        }
        print("难道在这？？？")

    except Exception as e:
        print(e)
    return render(request, "cart_manage/shopcart.html", context)


# 根据url的id参数获取商品并添加到购物车
def add_to_cart(request, product_id):
    try:
        print("你来了吗？")
        product = Product.objects.get(pk=product_id)
        print(product.product_title)
        carts = request.session.get("carts", None)
        if not carts:
            carts = Cart()
            request.session["carts"] = carts
        carts.add_product(product)
        request.session["carts"] = carts

    except Exception as e:
        print(e)
    print("你来了？")
    return render(request, "product_manage/index.html", locals())


# 清空购物车
def clean_cart(request):
    # 将session中的carts重置为空对象
    request.session["carts"] = Cart()
    # 返回商城首页
    return render(request, "product_manage/index.html", locals())