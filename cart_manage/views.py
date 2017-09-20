from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from cart_manage.models import Cart, LineItem
from product_manage.models import Product
from cart_manage.forms import ProductAddToCartForm


# Create your views here.
class Cart(object):
    def __init__(self, *args, **kwargs):
        self.items = []
        self.total_price = []

    def add_product(self, product):
        self.total_price += product.product_price
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += 1
                return self.items.append(LineItem(product=product, unit_price=product.product_price, quantity=1))


def view_cart(request):
    # 试图获取sessi中的购物车
    carts = request.session.get("cart", None)
    t = get_template("cart_manage/shopcart.html")
    # 如果session中没有购物车对象，则新创建一个并且把它加到session中
    if not carts:
        carts = Cart()
        request.session["carts"] = carts

    c = RequestContext(request, locals())

    return HttpResponse(t.render(c))


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