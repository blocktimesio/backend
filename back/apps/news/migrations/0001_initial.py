# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-09 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RankConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_shares', models.DecimalField(decimal_places=5, default=2.0, max_digits=9)),
                ('linkedin_shares', models.DecimalField(decimal_places=5, default=1.5, max_digits=9)),
                ('reddit_up', models.DecimalField(decimal_places=5, default=3.0, max_digits=9)),
                ('twitter_shares', models.DecimalField(decimal_places=5, default=1.1, max_digits=9)),
                ('views', models.DecimalField(decimal_places=5, default=2.0, max_digits=9)),
                ('comments', models.DecimalField(decimal_places=5, default=5.0, max_digits=9)),
                ('date_elapsed_seconds', models.PositiveIntegerField(default=3600)),
                ('date_coef', models.DecimalField(decimal_places=5, default=10, max_digits=9)),
            ],
            options={
                'verbose_name': 'Rank formula config',
            },
        ),
    ]
