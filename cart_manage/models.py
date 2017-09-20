from django.db import models
from product_manage.models import Product


# Create your models here.
class LineItem(models.Model):
    product = models.ForeignKey()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()


class Cart(models.Model):
    cart_id = models.CharField(max_length=50)
    data_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, unique=False)

    class Meta:
        db_table = "cart"
        ordering = ["data_added"]

    def total(self):
        return self.quantity * self.product.product_price

    def name(self):
        return self.product.product_title

    def price(self):
        return self.product.product_price

    def get_absolute_url(self):
        return self.product.product_image

    def augment_quantity(self, quantity):
        self.quantity += int(quantity)
        self.save()
