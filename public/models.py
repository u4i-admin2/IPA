from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from adminsortable.models import SortableMixin
from image_cropping import ImageRatioField


class Page(SortableMixin):
    site = models.CharField(
        max_length=3,
        choices=(
            ('aea', 'Atlas Agahi'),
            ('ipa', 'Iran Prison Atlas'),
        ),
        default='ipa',
    )

    slug = models.SlugField(_('Slug'), max_length=100)
    title = models.CharField(_('Title'), max_length=200)
    content = models.TextField(_('content'))
    modified_date = models.DateTimeField(auto_now=True, null=True)
    order = models.PositiveIntegerField(
        default=0, editable=False, db_index=True)
    is_published = models.BooleanField(default=True)
    image = models.ImageField(blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '1200x400')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ['order']
