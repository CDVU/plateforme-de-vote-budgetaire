# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-08 11:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_auto_20160408_0611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='accepted',
        ),
    ]
