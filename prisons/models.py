"""
Editable Types
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

import core_types.models
import core_types.managers


class Prison(core_types.models.PublishableMixin, models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255)

    address = models.TextField(
        verbose_name=_('Address'),
        max_length=255)

    dean_name = models.CharField(
        verbose_name=_('Dean Name'),
        max_length=255,
        null=True,
        blank=True)

    dean_email = models.EmailField(
        verbose_name=_('Dean E-mail'),
        max_length=255,
        blank=True,
        null=True)

    dean_phone = models.CharField(
        verbose_name=_('Dean Telephone'),
        max_length=255,
        null=True,
        blank=True)

    capacity = models.PositiveIntegerField(
        verbose_name=_('Capacity'),
        null=True,
        blank=True)

    capacity_is_estimate = models.BooleanField(
        verbose_name=_('Estimated Capacity'),
        default=False)

    latitude = models.FloatField(
        verbose_name=_('Latitude'),
        null=True,
        blank=True)

    longitude = models.FloatField(
        verbose_name=_('Longitude'),
        null=True,
        blank=True)

    opened_year = models.IntegerField(
        verbose_name=_('Year Of Opening'),
        null=True,
        blank=True)

    opened_month = models.IntegerField(
        verbose_name=_('Month Of Opening'),
        null=True,
        blank=True)

    opened_day = models.IntegerField(
        verbose_name=_('Day Of Opening'),
        null=True,
        blank=True)

    opened_year_fa = models.IntegerField(
        verbose_name=_('Persian Year Of Opening'),
        null=True,
        blank=True)

    opened_month_fa = models.IntegerField(
        verbose_name=_('Persian Month Of Opening'),
        null=True,
        blank=True)

    opened_day_fa = models.IntegerField(
        verbose_name=_('Persian Day Of Opening'),
        null=True,
        blank=True)

    ADMINISTERED_BY_CHOICES = [
        ('moi', _('Ministry of Information')),
        ('police', _('Police')),
        ('irgc', _('IRGC')),
        ('pdotj', _('Prisons Division of the Judiciary'))
    ]
    administered_by = models.CharField(
        verbose_name=_('Administered By'),
        choices=ADMINISTERED_BY_CHOICES,
        max_length=8,
        null=True,
        blank=True)

    physical_structure = models.TextField(
        verbose_name=_('Physical Structure'),
        null=True,
        blank=True)

    size_and_density = models.TextField(
        verbose_name=_('Size And Density'),
        null=True,
        blank=True)

    medicine_and_nutrition = models.TextField(
        verbose_name=_('Medicine And Nutrition'),
        null=True,
        blank=True)

    facilities = models.ManyToManyField(
        'PrisonFacility',
        verbose_name=_('Prison Facility'),
        blank=True)

    picture = models.ImageField(
        verbose_name=_('Prison Picture'),
        upload_to='prison_pics',
        null=True,
        blank=True)

    bio = models.TextField(
        verbose_name=_('Bio'),
        null=True,
        blank=True)

    explanation_en = models.TextField(
        verbose_name=_('Any extra explanation needed to be added to this '
                       'prisoner'),
        null=True,
        blank=True)

    explanation_fa = models.TextField(
        verbose_name=_('Any extra explanation needed to be added to this '
                       'prisoner'),
        null=True,
        blank=True)

    explanation_aea_en = models.TextField(
        verbose_name=_('Any extra explanation needed to be added to this '
                       'prisoner'),
        null=True,
        blank=True)

    explanation_aea_fa = models.TextField(
        verbose_name=_('Any extra explanation needed to be added to this '
                       'prisoner'),
        null=True,
        blank=True)

    objects = models.Manager()
    published_objects = core_types.managers.PublishedManager()

    class Meta:
        verbose_name = _('Prison')

    def __unicode__(self):
        return u'%s %s: %s' % (
            type(self).__name__,
            self.pk,
            self.name)

    # To be used to calculate prisons mistreatments
    # def update_mistreatment(self):
    #     """
    #     Update number of mistreatments for this judge
    #     """
    #     from prisoners.models import PrisonerArrest, PrisonerDetention
    #     from report.models import Report, ReportDetention

    #     arrests = PrisonerArrest.published_objects.filter(
    #         id__in=self.sentences.filter(is_published=True).values_list('arrest__id'))
    #     self.mistreatments_count = PrisonerDetention.published_objects.filter(
    #         arrest_id__in=arrests).aggregate(
    #             total_mistreatments=Count('treatment'))['total_mistreatments']

    #     reports = Report.published_objects.filter(
    #         id__in=self.report_sentences.filter(is_published=True).values_list('report__id'))
    #     self.aea_mistreatments_count = ReportDetention.published_objects.filter(
    #         report_id__in=reports).aggregate(
    #             total_mistreatments=Count('treatment'))['total_mistreatments']

    #     self.save()

    @classmethod
    def prefetch_queryset(cls, queryset):
        """
        Update a queryset to prefetch all related data for a prison.
        """
        return (queryset
                .prefetch_related('facilitylinks')
                .prefetch_related('facilities')
                .prefetch_related('files')
                .prefetch_related('quotes')
                .prefetch_related('sources')
                .prefetch_related('timeline')
                .prefetch_related('comments'))


class PrisonComment(core_types.models.Comment):
    prison = models.ForeignKey(
        'Prison',
        related_name='comments')


class PrisonSource(core_types.models.Source):
    prison = models.ForeignKey(
        'Prison',
        related_name='sources')

    class Meta:
        unique_together = [
            ('prison', 'name'),
        ]


class PrisonQuote(core_types.models.Quote):
    prison = models.ForeignKey(
        'Prison',
        related_name='quotes')


class PrisonFile(core_types.models.File):
    prison = models.ForeignKey(
        'Prison',
        related_name='files')

    FILE_TYPE_CHOICES = [
        ('visual_records', _('Visual records')),
        ('mistreatments', _('Mistreatments')),
        ('testimonials', _('Testimonials')),
        ('campaigns', _('Campaigns')),
    ]

    file_type = models.CharField(
        choices=FILE_TYPE_CHOICES,
        max_length=16,
    )


class PrisonTimeline(core_types.models.Timeline):
    prison = models.ForeignKey(
        'Prison',
        related_name='timeline')


class PrisonFacility(core_types.models.Choice):
    class Meta:
        verbose_name = _('Prison Facility')


class PrisonFacilityLink(core_types.models.PublishableMixin, models.Model):
    prison = models.ForeignKey(
        'Prison',
        related_name='facilitylinks')
    facility = models.ForeignKey(
        'PrisonFacility')
    description = models.CharField(max_length=255, null=True, blank=True)
