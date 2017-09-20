from django.http import response
from django.shortcuts import render
from product_manage.models import Product, Category
from cart_manage.models import Cart
from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage


# 分页
def get_paginator(list_to_page, num_per_page):
    try:
        # 创建分页对象
        paginator = Paginator(list_to_page, num_per_page)
        # 返回Page对象，包含商品信息
        page = int(request.GET.get("page", 1))
        list_to_page = paginator.page()
    except PageNotAnInteger as e:
        page = paginator.page(1)
    except EmptyPage as e:
        page = paginator.page(1)

    return list_to_page


# 首页
def index(request):
    context = {
        "guest_cart": 1,
        "title": "首页"
    }

    # 获得最火的4个商品(根据点击量从高到低排列)
    hottest_products = Product.objects.all().order_by("-product_click")[:4]
    context.setdefault("hottest_products", hottest_products)

    # ****获得各分类下的点击商品************
    # 先获得所有分类
    category_list = Category.objects.all()
    for i in range(len(category_list)):
        # 获得category对象
        category = category_list[i]
        # 根据目录获得商品列表
        # 根据id倒叙排列
        product_by_id = category.product_set.order_by("-id")[0:4]
        # 根据点击量倒叙排列
        product_by_click = category.product_set.order_by("-product_click")[0:4]
        # 主键
        key_by_id = str(category) + str(i)
        key_by_click = str(category) + str(i) + str(i)

        context.setdefault(key_by_id, product_by_id)
        context.setdefault(key_by_click, product_by_click)

    return render(request, "product_manage/index.html", context)


# 商品列表界面，接收category，id，排序方式，分页等参数
def list_products(request, category_id, sid, pindex):
    category = Category.objects.get(pk=int(category_id))
    news = category.product_set.order_by("id")[0:2]
    if sid == '1':
        # 按时间最新的排列
        product_list = category.product_set.order_by("-id")
    elif sid == '2':
        # 按价格排列
        product_list = Product.objects.filter(category_id=int(category_id)).order_by("-product_price")
    elif sid == '3':
        # 按点击量排列
        product_list = Product.objects.filter(category_id=int(category_id)).order_by("-product_click")

    # 调用分页的函数，每页显示10条记录
        product_list = get_paginator(product_list, 10)

    context = {
        "title": "商品列表",
        "guest_cart": 1,
        "product_list": product_list,
        "category": category,
        "sort": sid,
        "news": news,
    }

    return render(request, "product_manage/list.html", context)


# 根据商品id查询并展示商品详情
def detail(request, product_id):
    try:
        # filter返回的是queryset对象，get返回的才是索要查询的对象
        product = Product.objects.get(pk=product_id)

    except Exception as e:
        print(e)

    # 将商品id存入cookies
    response.set_cookie("product_id", product_id)
    return render(request, "product_manage/detail.html", locals())


# 商品展示
def product_detail(request, id):
    product = Product.objects.filter(pk=int(id)).first()
    # 点击量+1
    product.product_click += 1
    product.save()
    # 显示购物车的商品总数
    cart_count = Cart.objects.filter(user_id=request.session.get("uid")).count()
    news = product.product_category.product_set.order_by("-id")[0:2]
    context = {
        "title": product.product_category.catrgory,
        "product": product,
        "cart_count": cart_count,
        "news": news,
        "guest_cart": 1,
        "category": product.product_category
    }

    response = render(request, "product_manage/detail.html", context)

    # 接下来，要将浏览信息，存入 cookie ，以便 最近浏览 功能使用
    # 存入 cookie 的形式为 { 'gooids':'1,5,6,7,8,9'}
    product_ids = request.COOKIES.get("product_ids")
    if product_ids != "":
        # 将字符串拆分为列表
        product_ids_list = product_ids.split(",", "")
        # 判断id是否已经在列表里
        if product_ids_list.count(id) >= 1:
            # 若已存在就删除，再插入新的
            product_ids_list.remove(id)
        # 将新的id放在 列表的 第一个
        product_ids_list.insert(0, id)
        # 如果超过 6个，则删除最后一个，相当于长度为5的队列
        if len(product_ids_list) >= 6:
            del product_ids_list[5]
        # 将列表，以逗号分割的形式 拼接为字符串
        product_ids = ",".join(product_ids_list)

    else:
        # 如果为空则直接添加
        product_ids = id

    response.set_cookie("product_ids", product_ids)

    return response
