# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-19 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songwriter', '0008_auto_20170910_2249'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='harmonization',
            options={'ordering': ['verse', 'start_spot_in_verse']},
        ),
        migrations.RenameField(
            model_name='harmonization',
            old_name='spot_in_verse',
            new_name='start_spot_in_verse',
        ),
        migrations.AddField(
            model_name='harmonization',
            name='end_spot_in_verse',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
