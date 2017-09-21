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
    # 试图获取session中的购物车
    carts = request.session.get("carts", None)
    t = get_template('cart_manage/shopcart.html')
    # 如果session中没有购物车对象，则新创建一个并且把它加到session中
    if not carts:
        carts = Cart()
        request.session["carts"] = carts

    context = {
        "carts_id": carts,
    }

    return render(request, "cart_manage/shopcart.html", context)


# 根据url的id参数获取商品并添加到购物车
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    carts = request.session.get("carts", None)
    if not carts:
        carts = Cart()
        request.session["carts"] = carts
    carts.add_product(product)
    request.session["carts"] = carts

    return view_cart(request)


# 清空购物车
def clean_cart(request):
    request.session["carts"] = Cart()
    return view_cart(request)


def cart(request):
    user_id = request.session.get("user_id")
    carts = Cart.objects.filter(user_id=user_id)

    context = {
        "title": "购物车",
        "name": 1,
        "cart": carts
    }

    return render(request, "cart_manage/shopcart.html", context)


# 购物车显示商品
def show_product(request, product_slug):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.product_category.filter(is_active=True)
    page_title = p.product_title
    meta_keywords = p.meta_description
    meta_description = p.meta_description
    form = ProductAddToCartForm(request)

    return render(request, "cart_manage/shopcart.html", locals())


# 购物车编辑功能,传入 cart id 和 count 改变Cart
def edit(request, cart_id, product_count):
    try:
        cart = Cart.objects.get(pk=int(cart_id))
        cart.count = int(product_count)
        cart.save()

    except Exception as e:
        # 如果错误就将原来的数量返回去
        return JsonResponse({"count": product_count})

    return JsonResponse({"count": 0})


# 购物车删除功能
def delete(request, cart_id):
    try:
        cart = Cart.objects.get(pk=int(cart_id))
        cart.delete()
        data = {"ok": 1}
    except:
        data = {"ok": 0}

    return JsonResponse(data)