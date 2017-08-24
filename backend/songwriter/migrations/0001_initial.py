# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-04 14:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, default='', max_length=150)),
                ('lastname', models.CharField(blank=True, default='', max_length=150)),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
            ],
        ),
        migrations.CreateModel(
            name='Chord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(default='', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=150)),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
            ],
        ),
        migrations.CreateModel(
            name='Harmonization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spot_in_verse', models.PositiveIntegerField()),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
                ('chord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='songwriter.Chord')),
            ],
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('is_refrain', models.BooleanField(default=False, verbose_name='Is a refrain paragraph?')),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=150)),
                ('rights_paid', models.BooleanField(default=True, verbose_name='rights paid')),
                ('secli_number', models.CharField(blank=True, default='', max_length=150)),
                ('sacem_number', models.CharField(blank=True, default='', max_length=150)),
                ('comments', models.TextField(verbose_name='Comments')),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='songwriter.Author')),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='songwriter.Editor')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150)),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
            ],
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('content', models.TextField()),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='songwriter.Theme'),
        ),
        migrations.AddField(
            model_name='paragraph',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paragraphs', to='songwriter.Song'),
        ),
        migrations.AddField(
            model_name='harmonization',
            name='verse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='harmonizations', to='songwriter.Verse'),
        ),
    ]