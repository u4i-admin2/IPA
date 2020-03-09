# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-09-27 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0018_auto_20150814_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='prison',
            name='explanation_aea_en',
            field=models.TextField(blank=True, null=True, verbose_name='Any extra explanation needed to be added to this prisoner'),
        ),
        migrations.AddField(
            model_name='prison',
            name='explanation_aea_fa',
            field=models.TextField(blank=True, null=True, verbose_name='Any extra explanation needed to be added to this prisoner'),
        ),
        migrations.AddField(
            model_name='prison',
            name='explanation_en',
            field=models.TextField(blank=True, null=True, verbose_name='Any extra explanation needed to be added to this prisoner'),
        ),
        migrations.AddField(
            model_name='prison',
            name='explanation_fa',
            field=models.TextField(blank=True, null=True, verbose_name='Any extra explanation needed to be added to this prisoner'),
        ),
        migrations.AddField(
            model_name='prisontimeline',
            name='source_link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Source Link'),
        ),
        migrations.AlterField(
            model_name='prison',
            name='facilities',
            field=models.ManyToManyField(blank=True, to='prisons.PrisonFacility', verbose_name='Prison Facility'),
        ),
        migrations.AlterField(
            model_name='prisontimeline',
            name='description',
            field=models.TextField(max_length=1024, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='prisontimeline',
            name='description_en',
            field=models.TextField(max_length=1024, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='prisontimeline',
            name='description_fa',
            field=models.TextField(max_length=1024, null=True, verbose_name='Description'),
        ),
    ]