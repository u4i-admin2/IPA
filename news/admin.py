# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from core_types.admin import PUBLISHABLE_READONLY_FIELDS
from .models import FeaturedNews


class FeaturedNewsAdmin(admin.ModelAdmin):

    model = FeaturedNews

    list_display = ['title', 'is_published', 'featured']
    list_editable = ['is_published', 'featured']
    search_fields = ['excerpt']
    readonly_fields = PUBLISHABLE_READONLY_FIELDS


admin.site.register(FeaturedNews, FeaturedNewsAdmin)
