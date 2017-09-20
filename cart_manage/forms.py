from django import forms

class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(label="数量", widget=forms.TextInput(
        attrs={
            'size': '2',
            'value': '1',
            'class': 'quantity',
            'max_length': 5,
        }), error_messages={"invalid": "请输入有效数量"},min_value=1,)

    product_slug = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 检查用户浏览器端cookie是否开启
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("需要启用cookie")

        return self.cleaned_data
