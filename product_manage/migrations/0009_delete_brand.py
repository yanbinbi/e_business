# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 05:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_manage', '0008_auto_20170921_1334'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Brand',
        ),
    ]