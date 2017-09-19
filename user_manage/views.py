from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from user_manage.models import User
from product_manage.models import Product
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout, login, authenticate
from user_manage.forms import LoginForm, RegForm


# 登录装饰器
# def login(func):
#     def login_fun(request, *args, **kwargs):
#         if request.session.has_key("user_name"):
#             # 如果登录成功，继续执行原函数
#             return func(request, *args, **kwargs)
#         else:
#             red = HttpResponseRedirect("/user/login")
#             red.set_cookie("url", request.get_full_path())
#             return red
#     return login_fun


# 登录视图函数
# def login(request):
#     # 获取cookies里的用户名和密码，实现自动填写功能
#     user_name = request.COOKIES["user_name"]
#     user_password = request.COOKIES["user_password"]
#     context = {
#         "user_name": user_name,
#         "user_password": user_password,
#         "error": 0
#     }
#
#     try:
#         # 获取头部的来源地址
#         url = request.META["HTTP_REFERER"]
#     except Exception as e:
#         url = "/"
#
#     # render方法返回 httpresponse
#     response = render(request, "user_manage/login.html", context=context)
#     # 将请求的url存入cookie，登录后返回原先的页面
#     response.set_cookie("url", url)
#     return response


# 登录处理函数
def login_handle(request):
    try:
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 接受表单数据
                user_name = login_form.cleaned_data["user_name"]
                user_password = login_form.cleaned_data["user_password"]
                # 设置默认值
                # remember = login_form.cleaned_data["remember"]
                # 判断要登录的用户名是否存在
                has_user = User.objects.filter(user_name=user_name)
                # 如果没有该用户
                if not has_user:
                    context = {
                        "error": "该用户不存在",
                        "user_name": user_name
                    }
                    return render(request, "user_manage/login.html", context=context)
                # 加密
                s_user_password = make_password(user_password)
                user = authenticate(user_name__exact=user_name, user_password__exact=s_user_password)
                # 验证用户是否正确
                if user:
                    # 第二个参数为默认参数，如果url没有，则跳转到首页
                    url = request.COOKIES.get("url", "/")
                    red = HttpResponseRedirect(url)
                    # 如果记住密码则将用户名和密码写入cookies
                    # if remember == '1':
                    #     red.set_cookie("user_name", user_name)
                    #     red.set_cookie("user_password", user_password)
                    # else:
                    #     red.set_cookie("user_name", "", max_age=-1)
                    #     red.set_cookie("user_password", "", max_age=-1)
                    #     # 写入cookies
                    #     request.COOKIES["user_info"] = [user.user_name, user.user_name]

                    # 将user_name和id写入session，以保持登录状态
                    request.session["user_name"] = user_name
                    request.session["user_id"] = user.id

                    return red
                else:
                    # 用户存在但是密码错误，给出错误信息并返回登录界面
                    context = {
                        "error": "密码错误",
                        "user_name": user_name
                    }

                    return render(request, "user_manage/login.html", context=context)
            else:
                # 输入的数据无效
                context = {
                    "error": "输入的数据不符合要求"
                }
        else:
            login_form = LoginForm()
    except Exception as e:
        print(e)

    return render(request, "user_manage/login.html", locals())


# 注册处理函数
def register_handle(request):
    try:
        if request.method == "POST":
            register_form = RegForm(request.POST)
            if register_form.is_valid():
                # 接收用户输入
                user_name = register_form.cleaned_data["user_name"]
                user_password = register_form.cleaned_data["user_password"]
                repeat_user_password = register_form.cleaned_data["repeat_user_password"]
                user_email = register_form.cleaned_data["user_email"]
                user_phone = register_form.cleaned_data["user_phone"]

                # 判断注册的用户是否已经存在
                is_exits = User.objects.filter(user_name__exact=user_name).first()
                if is_exits:
                    context = {
                        "error": "用户名已经存在"
                    }
                # 判断两次输入的密码是否相等
                elif user_password != repeat_user_password:
                    context = {
                        "error": "两次输入的密码不一致，请重新输入"
                    }

                    return render(request, "user_manage/register.html", context=context)

                # 创建用户对象并持久化到数据库
                user = User.objects.create(
                    user_name=user_name,
                    user_password=user_password,
                    user_email=user_email,
                    user_phone=user_phone
                )

                user.save()
                # 采用django自带的登录用户
                # user.backend = "django.contrib.auth.backends.ModelBackend"
                # login(request, user)
                # print("已登录")
                return render(request, "product_manage/index.html", locals())
            else:
                return render(request, "user_manage/register.html", locals())

        else:
            register_form = RegForm()
    except Exception as e:
        print(e)

    return render(request, "user_manage/register.html", locals())


# 注册用户已存在
def register_exist(request):
    user_name = request.GET.get("user_name")
    count = User.objects.filter(user_name=user_name).count()
    # 返回json字典，判断是否存在
    return JsonResponse({"count": count})


# 注销
def logout_handle(request):
    logout(request)
    return redirect("/")


# 展示用户信息

def user_center_info(request):
    try:
        user_name = request.session.get("user_name")
        user = User.objects.filter(user_name__exact=user_name)

        # 从cookie中获取最近浏览的商品
        product_ids = request.COOKIES.get("product_ids")
        if product_ids != "":
            # 拆分为Id的列表
            product_id_list = product_ids.split(",")
            # 定义用于存放商品的列表
            product_list = []
            for product_id in product_ids:
                product = Product.objects.get(pk__exact=product_id)
                product_list.append(product)
        else:
            product_list = []

        context = {
            "title": "用户中心",
            "user_name": user_name,
            "user_phone": user.phone,
            "user_address": user.user_address,
            "product_list": product_list,
            "tag": 1  # tag标记，高亮页
        }

    except Exception as e:
        print(e)

    return render(request, "user_manage/user_center_info.html", context)


# 个人信息--收货地址
def user_center_site(request):
    try:
        user_name = request.session.get("user_name")
        user = User.objects.filter(user_name__exact=user_name)
        # 提交方式为POST时进行修改
        if request.method == "POST":
            user_address = request.POST.get("user_address")
            user_name = request.POST.get("user_name")
            user_phone = request.POST.get("user_phone")
            # 修改用户信息
            user.user_address = user_address
            user.user_name = user_name
            user.user_phone = user_phone
            user.save()

        context = {
            "user_address": user.user_address,
            "user_name": user.user_name,
            "user_phone": user.user_phone,
            "tag": 3
        }

    except Exception as e:
        print(e)

    return render(request, "user_manage/user_center_site.html", context)


# 订单
def user_center_order(request):
    pass




