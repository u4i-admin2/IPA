# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-09-27 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0009_auto_20150814_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge',
            name='aea_mistreatments_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='judge',
            name='explanation_aea_en',
            field=models.TextField(blank=True, null=True, verbose_name='Any extra explanation needed to be added to this prisoner'),
        ),
        migrations.AddField(
            model_name='judge',
            name='explanation_aea_fa',
            field=models.TextField(blank=True, null=True, verbose_name='Any extra explanation needed to be added to this prisoner'),
        ),
        migrations.AddField(
            model_name='judge',
            name='explanation_en',
            field=models.TextField(blank=True, null=True, verbose_name='Any extra explanation needed to be added to this prisoner'),
        ),
        migrations.AddField(
            model_name='judge',
            name='explanation_fa',
            field=models.TextField(blank=True, null=True, verbose_name='Any extra explanation needed to be added to this prisoner'),
        ),
        migrations.AddField(
            model_name='judge',
            name='is_judge',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='judge',
            name='mistreatments_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='judgetimeline',
            name='source_link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Source Link'),
        ),
        migrations.AlterField(
            model_name='judgetimeline',
            name='description',
            field=models.TextField(max_length=1024, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='judgetimeline',
            name='description_en',
            field=models.TextField(max_length=1024, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='judgetimeline',
            name='description_fa',
            field=models.TextField(max_length=1024, null=True, verbose_name='Description'),
        ),
    ]
