# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-07 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songwriter', '0016_auto_20171124_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='theme',
            field=models.ManyToManyField(blank=True, to='songwriter.Theme'),
        ),
    ]
