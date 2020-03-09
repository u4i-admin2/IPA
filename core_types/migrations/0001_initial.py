# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core_types.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('is_published', models.BooleanField(default=False, db_index=True, verbose_name='Approved for publishing?')),
                ('name', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_fa', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_en', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('located_in_iran', models.BooleanField(default=False, verbose_name='Is located in Iran')),
                ('created_by', models.ForeignKey(related_name='+', default=core_types.utils.get_request_user, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Created By')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('is_published', models.BooleanField(default=False, db_index=True, verbose_name='Approved for publishing?')),
                ('name', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_fa', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_en', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('created_by', models.ForeignKey(related_name='+', default=core_types.utils.get_request_user, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(related_name='+', verbose_name='Last Updated By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ethnicity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('is_published', models.BooleanField(default=False, db_index=True, verbose_name='Approved for publishing?')),
                ('name', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_fa', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_en', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('created_by', models.ForeignKey(related_name='+', default=core_types.utils.get_request_user, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(related_name='+', verbose_name='Last Updated By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Ethnicity',
                'verbose_name_plural': 'Ethnicities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('is_published', models.BooleanField(default=False, db_index=True, verbose_name='Approved for publishing?')),
                ('name', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_fa', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_en', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('created_by', models.ForeignKey(related_name='+', default=core_types.utils.get_request_user, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(related_name='+', verbose_name='Last Updated By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Province',
                'verbose_name_plural': 'Provinces',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('is_published', models.BooleanField(default=False, db_index=True, verbose_name='Approved for publishing?')),
                ('name', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_fa', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('name_en', models.CharField(max_length=255, unique=True, null=True, verbose_name='Name', blank=True)),
                ('created_by', models.ForeignKey(related_name='+', default=core_types.utils.get_request_user, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(related_name='+', verbose_name='Last Updated By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Religion',
                'verbose_name_plural': 'Religions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(verbose_name='Province', blank=True, to='core_types.Province', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='updated_by',
            field=models.ForeignKey(related_name='+', verbose_name='Last Updated By', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
