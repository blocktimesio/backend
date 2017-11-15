# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flatpage',
            name='url',
        ),
        migrations.AddField(
            model_name='flatpage',
            name='slug',
            field=models.SlugField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
