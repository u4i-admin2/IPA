from django.db import models


class TagList(models.Model):
    """
    This dummy model is used to allow exporting a /module/taglist as a ViewSet,
    without having to write a metric ton of custom code. No instances of it are
    ever created.
    """


class SearchTestModel(models.Model):
    """
    This dummy model exists solely to allow api/tests.py:SearchViewSetTestCase
    to ensure Watson correctly indexes and searches results.
    """
    text = models.CharField(max_length=255)

    @classmethod
    def prefetch_queryset(cls, queryset):
        return queryset

    @property
    def url(self):
        return 'http://test-url/'
