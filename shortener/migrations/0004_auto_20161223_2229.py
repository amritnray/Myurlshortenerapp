# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-23 16:59
from __future__ import unicode_literals

from django.db import migrations, models
import shortener.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_auto_20161221_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kirrurl',
            name='url',
            field=models.CharField(max_length=220, validators=[shortener.validators.validate_url, shortener.validators.validate_dot_com]),
        ),
    ]
