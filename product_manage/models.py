from django.db import models
from tinymce.models import HTMLField


# 分类表
class Category(models.Model):
    category = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.category


# 品牌表
class Brand(models.Model):
    brand = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.brand


# 商品类
class Product(models.Model):
    product_title = models.CharField(max_length=50)
    # 图片(地址)存储目录
    product_image = models.ImageField(upload_to="static/productImage")
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    product_unit = models.CharField(max_length=20, default="500g")
    product_click = models.IntegerField(verbose_name="点击量")
    product_description = models.CharField(verbose_name="简介", max_length=100)
    product_detail = HTMLField()
    product_category = models.ForeignKey(Category)
    # product_brand = models.ForeignKey(Brand, null=True)
    product_remain = models.IntegerField(verbose_name="库存", default=0)

    def __str__(self):
        return self.product_title
