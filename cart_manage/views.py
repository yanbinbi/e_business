from django.http import JsonResponse
from django.shortcuts import render, redirect
from cart_manage.models import Cart


# Create your views here.
def add(request, product_id, product_count):
    product_id = int(product_id)
    product_count = int(product_count)
    user_id = request.session.get("user_id")
    carts = Cart.objects.filter(product_id=product_id, user_id=user_id)
    # 先判断 该用户 购物车中 是否 存在 该商品
    # 如果纯在，则仅作数量上的 加法
    if len(carts) >= 1:
        cart = carts[0]
        cart.count += product_count
    # 不存在就创建该商品
    else:
        cart = Cart()
        cart.user_id = user_id
        cart.product_id = product_id
        cart.count = product_count

    cart.save()
    # 判断请求方式 是否是ajax，若是则返回json格式的 商品数量即可
    if request.is_ajax():
        count = Cart.objects.filter(user_id=user_id).count()
        return JsonResponse({"count": count})

    else:
        return redirect("/cart")


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