# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.db.models import Q
from user_manage.models import User
import re


# 登录表单
class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required", }),
                               max_length=50, error_messages={"required": "username不能为空", })
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
                               max_length=20, error_messages={"required": "password不能为空", })


# 注册表单
class RegForm(forms.Form):
    """注册表单"""
    user_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    user_email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                              max_length=50,error_messages={"required": "email不能为空",})
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})
    repeat_user_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password",
                              "required": "required",}), max_length=20,error_messages={"required": "password不能为空",})

    user_phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=11,error_messages={"required": "username不能为空",})

