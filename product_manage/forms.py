from django.forms import ModelForm
from product_manage.models import Product


# 显示商品信息
class ProductDetailForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
