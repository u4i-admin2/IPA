# coding: utf-8

from django.core.cache import cache
from django.db import models


class SingletonModel(models.Model):

    def save(self, *args, **kwargs):
        self.pk = 1
        self.id = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    class Meta:
        abstract = True


class CloudFrontState(models.Model):
    should_invalidate_during_next_cron_tick = models.BooleanField(
        default=False
    )


class CsvState(SingletonModel):
    should_write_csv = models.BooleanField(
        default=False)
