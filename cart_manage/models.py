from django.db import models


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey("user_manage.User")
    product = models.ForeignKey("product_manage.Product")
    count = models.IntegerField()