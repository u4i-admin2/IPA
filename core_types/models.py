# coding: utf-8

"""
Editable types used for both judge and prisoners
"""

import threading

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _
from markdownx.utils import markdownify

import api.utils
import core_types.utils
from core_types.managers import PublishedManager


class PublishableMixin(models.Model):
    """
    Model mix-in that adds fields representing approved/unapproved state of
    some object.

    Django rest_framework API is configured to implement our permission rules
    if an object about to be modified inherits from this class. See
    api/viewsets.py.
    """
    created = models.DateTimeField(
        verbose_name=_('Created'),
        auto_now_add=True)

    updated = models.DateTimeField(
        verbose_name=_('Last Updated'),
        auto_now=True)

    created_by = models.ForeignKey(
        'auth.User',
        verbose_name=_('Created By'),
        default=core_types.utils.get_request_user,
        related_name='+',
        null=True,
        blank=True)

    updated_by = models.ForeignKey(
        'auth.User',
        verbose_name=_('Last Updated By'),
        related_name='+',
        null=True,
        blank=True)

    is_published = models.BooleanField(
        verbose_name=_('Approved for publishing?'),
        db_index=True,
        default=False)

    class Meta:
        abstract = True

    # We need to keep track of which models we're currently recursing into, to
    # avoid infinite loop as children try to mark their parent (me) published,
    # when I am trying to mark the child published.
    _published_tls = threading.local()

    def _mark_children_published(self):
        """
        Figure out all this model's related fields, then walk all of them and
        set their is_published=True.
        """
        try:
            in_progress = self._published_tls.in_progress
        except AttributeError:
            in_progress = self._published_tls.in_progress = set()

        if self.pk and self in in_progress:
            return

        if self.pk:
            in_progress.add(self)

        fields = api.utils.walk_model_fields(type(self))
        for kind, field_name, model_class in fields:
            # Skip over fields (like created_by) that aren't publishable.
            if not (model_class and issubclass(model_class, PublishableMixin)):
                continue

            if kind == 'foreign_key':
                child = getattr(self, field_name)
                if child:
                    child.is_published = True
                    # Saving the child causes pre_save() to fire for the child,
                    # which ends up recursively calling this function.
                    child.save()

            # Don't touch related or many-to-many until the model has been
            # written at least once else Django error.
            elif self.pk is not None and kind in ('related', 'many_to_many'):
                for child in getattr(self, field_name).all():
                    child.is_published = True
                    child.save()

        if self.pk:
            in_progress.discard(self)

    def _on_pre_save(sender, instance, raw, **kwargs):
        """
        If we're inside a web request and there is an authenticated user,
        automatically set updated_by.

        Additionally if we're about to save a PublishableMixin with
        is_published=True for the first time, then walk all its children and
        set their is_published=True too.
        """
        if raw:
            return

        if not isinstance(instance, PublishableMixin):
            return

        instance.updated_by = core_types.utils.get_request_user()
        if instance.is_published and (
            (instance.pk is None) or (
                not sender.objects.get(pk=instance.pk).is_published)):
            instance._mark_children_published()

    pre_save.connect(_on_pre_save)


class PublishablePublishedByDefaultModel(PublishableMixin):
    u"""
    GH 2019-08-23: This can be used in place of PublishableMixin to set up a
    PublishableMixin model with is_published = True by default.

    Note that this isn’t called PublishablePublishedByDefaultMixin since it and
    PublishableMixin are abstract classes, not mixins.

    Django’s model handling seems to have some weird quirks preventing mixins
    from working properly: https://stackoverflow.com/q/3254436/7949868
    """
    is_published = models.BooleanField(
        verbose_name=_('Approved for publishing?'),
        db_index=True,
        default=True)

    class Meta:
        abstract = True


class Choice(PublishableMixin, models.Model):
    # Note: use core_types.translation.ChoiceTranslationOptions.
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
        unique=True,
        null=True,
        blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s %s: %s' % (type(self).__name__, self.pk, self.name_en)


class Quote(PublishableMixin, models.Model):
    """
    Abstract base containing common fields and behaviours for quotes associated
    with an entity.
    """
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255)

    # Note: use core_types.translation.QuoteTranslationOptions.
    quote = models.CharField(
        verbose_name=_('Quote'),
        max_length=255)

    source = models.CharField(
        verbose_name=_('Source'),
        max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = _('Quote Evidence')
        verbose_name_plural = _('Quote Evidence')

    def __unicode__(self):
        return u'%s %s: %s' % (type(self).__name__, self.pk, self.quote)


class File(PublishableMixin, models.Model):
    """
    Abstract base containing common fields and behaviours for file evidence
    associated with an entity.
    """
    # Note: use core_types.translation.FileTranslationOptions.
    name = models.CharField(
        verbose_name=_('File Name'),
        max_length=255)

    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True)

    file = models.FileField(
        verbose_name=_('Data'),
        upload_to='file_evidence')

    file_thumb = models.ImageField(
        verbose_name=_('Thumbnail'),
        upload_to='file_evidence_thumbnails',
        null=True,
        blank=True)

    class Meta:
        abstract = True
        verbose_name = _('File Evidence')
        verbose_name_plural = _('File Evidence')

    def __unicode__(self):
        return u'%s %s: %s' % (type(self).__name__, self.pk, self.name)


class Timeline(PublishableMixin, models.Model):
    """
    Abstract base containing common fields and behaviours for timeline events
    associated with an entity.
    """
    # Note: use core_types.translation.TimelineTranslationOptions.
    year = models.IntegerField(
        verbose_name=_('Year Of Event'),
        null=True,
        blank=True)

    month = models.IntegerField(
        verbose_name=_('Month Of Event'),
        null=True,
        blank=True)

    day = models.IntegerField(
        verbose_name=_('Day Of Event'),
        null=True,
        blank=True)

    year_fa = models.IntegerField(
        verbose_name=_('Persian Year Of Event'),
        null=True,
        blank=True)

    month_fa = models.IntegerField(
        verbose_name=_('Persian Month Of Event'),
        null=True,
        blank=True)

    day_fa = models.IntegerField(
        verbose_name=_('Persian Day Of Event'),
        null=True,
        blank=True)

    timeline_is_estimate = models.NullBooleanField(
        verbose_name=_('Timeline Date Is Estimate?'),
        null=True,
        blank=True)

    source_link = models.CharField(
        verbose_name=('Source Link'),
        null=True,
        blank=True,
        max_length=255)

    description = models.TextField(
        verbose_name=_('Description'))

    class Meta:
        abstract = True
        verbose_name = _('Timeline Event')

    def __unicode__(self):
        return u'%s %s: %s/%s/%s %s' % (
            type(self).__name__,
            self.pk,
            self.year,
            self.month,
            self.day,
            self.description)

    @property
    def description_en_html(self):
        return markdownify(self.description_en)

    @property
    def description_fa_html(self):
        return markdownify(self.description_fa)


class Source(PublishableMixin, models.Model):
    """
    Abstract base containing fields common to all entity source references.
    """
    link = models.CharField(
        verbose_name=_('Link'),
        null=True,
        blank=True,
        max_length=255)

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255)

    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True)

    related_fields = models.CharField(
        verbose_name=_('Related Fields'),
        max_length=255,
        default='',
        help_text=_('''
            Comma-separated list of field names this source relates to.
        '''),
        blank=True)

    def _on_pre_save(sender, instance, raw, **kwargs):
        """
        Listen to attempts to save any Source subclass anywhere, dynamically
        verifying the list of fields in `related_fields` against the available
        fields for the specific subclass.
        """
        if raw:
            return

        if isinstance(instance, Source) and instance.related_fields:
            valid_tags = set(api.utils.extract_model_fields(sender.__module__))
            for tag in instance.related_fields.split(','):
                if tag not in valid_tags:
                    raise ValidationError(_('%r is not a valid tag for %s'
                                          % (tag, sender.__name__)))
    pre_save.connect(_on_pre_save)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s %s: %s' % (type(self).__name__, self.pk, self.name)


class Comment(models.Model):
    """
    Abstract base containing fields common to all entity "Conflicts And
    Considerations".
    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        null=True,
        default=core_types.utils.get_request_user)

    created = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Creation Date'))

    comment = models.TextField(
        verbose_name=_('Comment Text'))

    class Meta:
        abstract = True
        ordering = ('-created',)
        verbose_name = _('Conflicts And Considerations')
        verbose_name_plural = _('Conflicts And Considerations')

    def __unicode__(self):
        return u'%s %s: %s' % (type(self).__name__, self.pk, self.comment)


class City(Choice):
    province = models.ForeignKey(
        'Province',
        verbose_name=_('Province'),
        null=True,
        blank=True)

    located_in_iran = models.BooleanField(
        verbose_name=_('Is located in Iran'),
        default=False)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Country(Choice):
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class Ethnicity(Choice):
    class Meta:
        verbose_name = _('Ethnicity')
        verbose_name_plural = _('Ethnicities')


class Province(Choice):
    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')


class Religion(Choice):
    class Meta:
        verbose_name = _('Religion')
        verbose_name_plural = _('Religions')
