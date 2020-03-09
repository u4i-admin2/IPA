# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('title_fa', models.CharField(max_length=200, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=200, null=True, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('content_fa', models.TextField(null=True, verbose_name='content')),
                ('content_en', models.TextField(null=True, verbose_name='content')),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('order', models.PositiveIntegerField(default=0, editable=False, db_index=True)),
                ('is_published', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='uploaded_images', blank=True)),
                (b'cropping', image_cropping.fields.ImageRatioField('image', '1200x400', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
            bases=(models.Model,),
        ),
    ]
