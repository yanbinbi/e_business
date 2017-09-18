from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=30)
    user_address = models.CharField(max_length=100, default="")
    user_phone = models.CharField(max_length=11, default="")
    # 加密

    def save(self, *args, **kwargs):
        self.user_password = make_password(self.user_password, "ybb", "pbkdf2_sha256")
        super(User, self).save(*args, **kwargs)
