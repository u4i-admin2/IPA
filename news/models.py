# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from core_types.models import PublishableMixin
from core_types.managers import PublishedManager
from django.utils.translation import ugettext_lazy as _


class FeaturedNews(PublishableMixin, models.Model):

    LANGUAGE = [('en', _('English')),
                ('fa', _('Farsi'))]

    language = models.CharField(
        max_length=3,
        choices=LANGUAGE)

    title = models.CharField(
        max_length=256)

    excerpt = models.TextField()

    link = models.CharField(
        max_length=1024)

    photo = models.ImageField(
        upload_to='news_pics')

    featured = models.BooleanField(
        default=True)

    objects = models.Manager()
    published_objects = PublishedManager()

    def __unicode__(self):
        return self.title
