# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 10:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('magazines', '0002_auto_20160523_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='subscription_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 10, 27, 58, 645000, tzinfo=utc)),
        ),
    ]
