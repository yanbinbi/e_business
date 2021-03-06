# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 04:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_manage', '0001_initial'),
        ('user_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_manage.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_manage.User')),
            ],
        ),
    ]
