# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 04:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_manage', '0005_remove_product_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_brand',
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product_manage.Category'),
        ),
    ]
