# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-09-03 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='site',
            field=models.CharField(choices=[('aea', 'Atlas Agahi'), ('ipa', 'Iran Prison Atlas')], default='ipa', max_length=3),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='page',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='page',
            name='title_fa',
            field=models.CharField(max_length=200, null=True, verbose_name='Title'),
        ),
    ]
