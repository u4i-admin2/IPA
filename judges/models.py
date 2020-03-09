"""
Editable Types
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

import core_types.models
import core_types.managers


class Judge(core_types.models.PublishableMixin, models.Model):
    forename = models.CharField(
        verbose_name=_('First Name'),
        max_length=255,
        null=True,
        blank=True)

    surname = models.CharField(
        verbose_name=_('Surname'),
        max_length=255)

    dob_year = models.IntegerField(
        verbose_name=_('Birth Year (Gregorian)'),
        null=True,
        blank=True)

    dob_month = models.IntegerField(
        verbose_name=_('Birth Month (Gregorian)'),
        null=True,
        blank=True)

    dob_day = models.IntegerField(
        verbose_name=_('Birth Day (Gregorian)'),
        null=True,
        blank=True)

    dob_year_fa = models.IntegerField(
        verbose_name=_('Birth Year (Persian)'),
        null=True,
        blank=True)

    dob_month_fa = models.IntegerField(
        verbose_name=_('Birth Month (Persian)'),
        null=True,
        blank=True)

    dob_day_fa = models.IntegerField(
        verbose_name=_('Birth Day (Persian)'),
        null=True,
        blank=True)

    dob_is_estimate = models.NullBooleanField(
        verbose_name=_('Birth Date Is Estimate?'),
        null=True,
        blank=True)

    birth_city = models.ForeignKey(
        'core_types.City',
        verbose_name=_('Birth Village/City'),
        null=True,
        blank=True)

    birth_province = models.ForeignKey(
        'core_types.Province',
        verbose_name=_('Birth Province'),
        null=True,
        blank=True)

    ethnicity = models.ForeignKey(
        'core_types.Ethnicity',
        verbose_name=_('Ethnicity'),
        null=True,
        blank=True)

    picture = models.ImageField(
        verbose_name=_('Picture'),
        upload_to='judge_pics',
        null=True,
        blank=True)

    CLERIC_STATUS = [(True, _('Cleric')),
                     (False, _('Not cleric')),
                     (None, _('Unknown'))]
    is_cleric = models.NullBooleanField(
        verbose_name=_('Is Cleric?'),
        choices=CLERIC_STATUS,
        default=None)

    JUDGE_TYPE = [(None, _('Unknown')),
                  ('research', _('Research')),
                  ('primary', _('Primary')),
                  ('appeal', _('Appeal')),
                  ('supreme', _('Supreme'))]
    judge_type = models.CharField(
        verbose_name=_('Judge Type'),
        max_length=30,
        choices=JUDGE_TYPE,
        null=True,
        blank=True)

    judicial_position = models.ForeignKey(
        'JudicialPosition',
        verbose_name=_('Judge Type'),
        null=True,
        blank=True)

    court_and_branch = models.ForeignKey(
        'CourtAndBranch',
        verbose_name=_('Court and Branch'),
        null=True,
        blank=True)

    biography = models.TextField(
        verbose_name=_('Biography'),
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

    mistreatments_count = models.IntegerField(
        null=True,
        default=0)

    aea_mistreatments_count = models.IntegerField(
        null=True,
        default=0)

    is_judge = models.BooleanField(
        default=True)

    def get_name(self):
        first = self.forename or ''
        second = self.surname or ''
        name = "%s %s" % (first, second)
        return name.strip()

    objects = models.Manager()
    published_objects = core_types.managers.PublishedManager()

    class Meta:
        verbose_name = _('Judge')

    def __unicode__(self):
        return u'%#s: %s %s' %\
            (self.id,
             self.surname or u'',
             self.forename or u'')

    def judge_name_en(self):
        return u'%s %s' % \
            (self.surname_en or u'',
             self.forename_en or u'')

    def judge_name_fa(self):
        return u'%s %s' % \
            (self.surname_fa or u'',
             self.forename_fa or u'')

    @classmethod
    def prefetch_queryset(cls, queryset):
        """
        Update a queryset to prefetch all related data for a prison.
        """
        return (queryset
                .prefetch_related('court_and_branch')
                .prefetch_related('judicial_position')
                .prefetch_related('ethnicity')
                .prefetch_related('quotes')
                .prefetch_related('files')
                .prefetch_related('timeline')
                .prefetch_related('positions')
                .prefetch_related('sources')
                .prefetch_related('comments'))

    def update_mistreatment(self):
        """
        Update number of mistreatments for this judge
        """
        from prisoners.models import SentenceBehaviour
        from report.models import ReportSentenceBehaviour

        self.mistreatments_count = SentenceBehaviour.published_objects.filter(
            sentence_id__in=self.sentences.filter(is_published=True).values_list('id')).count()

        self.aea_mistreatments_count = ReportSentenceBehaviour.published_objects.filter(
            report_sentence_id__in=self.report_sentences.filter(is_published=True).values_list('id', flat=True)).count()

        self.save()


class JudgeComment(core_types.models.Comment):
    judge = models.ForeignKey(
        'Judge',
        related_name='comments')


class JudgeSource(core_types.models.Source):
    judge = models.ForeignKey(
        'Judge',
        related_name='sources')

    class Meta:
        unique_together = [
            ('judge', 'name'),
        ]


class JudgePosition(core_types.models.PublishableMixin, models.Model):
    judge = models.ForeignKey(
        'Judge',
        related_name='positions')

    court_and_branch = models.ForeignKey(
        'CourtAndBranch',
        verbose_name=_('Court and Branch'),
        null=True,
        blank=True)

    judicial_position = models.ForeignKey(
        'JudicialPosition',
        verbose_name=_('Judge Type'),
        null=True,
        blank=True)

    started_year = models.IntegerField(
        verbose_name=_('Term Started Year (Gregorian)'),
        null=True,
        blank=True)

    started_month = models.IntegerField(
        verbose_name=_('Term Started Month (Gregorian)'),
        null=True,
        blank=True)

    started_day = models.IntegerField(
        verbose_name=_('Term Started Day (Gregorian)'),
        null=True,
        blank=True)

    started_year_fa = models.IntegerField(
        verbose_name=_('Term Started Year (Persian)'),
        null=True,
        blank=True)

    started_month_fa = models.IntegerField(
        verbose_name=_('Term Started Month (Persian)'),
        null=True,
        blank=True)

    started_day_fa = models.IntegerField(
        verbose_name=_('Term Started Day (Persian)'),
        null=True,
        blank=True)

    ended_year = models.IntegerField(
        verbose_name=_('Term Ended Year (Gregorian)'),
        null=True,
        blank=True)

    ended_month = models.IntegerField(
        verbose_name=_('Term Ended Month (Gregorian)'),
        null=True,
        blank=True)

    ended_day = models.IntegerField(
        verbose_name=_('Term Ended Day (Gregorian)'),
        null=True,
        blank=True)

    ended_year_fa = models.IntegerField(
        verbose_name=_('Term Ended Year (Persian)'),
        null=True,
        blank=True)

    ended_month_fa = models.IntegerField(
        verbose_name=_('Term Ended Month (Persian)'),
        null=True,
        blank=True)

    ended_day_fa = models.IntegerField(
        verbose_name=_('Term Ended Day (Persian)'),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('Position')
        ordering = ('started_year', 'started_month', 'started_day')

    def __unicode__(self):
        return u'%s %s' % (type(self).__name__, self.pk)


class JudgeQuote(core_types.models.Quote):
    judge = models.ForeignKey(
        'Judge',
        related_name='quotes')


class JudgeFile(core_types.models.File):
    judge = models.ForeignKey(
        'Judge',
        related_name='files')

    FILE_TYPE_CHOICES = [
        ('rulings', _('Rulings')),
        ('verdicts', _('Verdicts')),
        ('transcripts', _('Transcripts')),
        ('campaigns', _('Campaigns')),
    ]

    file_type = models.CharField(
        choices=FILE_TYPE_CHOICES,
        max_length=16,
    )


class JudgeTimeline(core_types.models.Timeline):
    judge = models.ForeignKey(
        'Judge',
        related_name='timeline')


class SentenceType(core_types.models.Choice):
    class Meta:
        verbose_name = _('Sentence Type')

    finality = models.IntegerField(
        verbose_name=_('Finality'),
        default=0,
        help_text=_('Finality of the sentence, i.e. how important '
                    'this judgement is relative to other judgements '
                    'made as part of the same arrest. The sentence '
                    'whose type has the highest finality dictates the '
                    'ultimate sentence length.'))


class BehaviourType(core_types.models.Choice):
    class Meta:
        verbose_name = _('Type of Judicial Behaviour')


class JudicialPosition(core_types.models.Choice):
    """
    Ie prosecutor etc etc.
    """
    class Meta:
        verbose_name = _('Judicial Position')
        verbose_name_plural = _('Judicial Positions')


class CourtAndBranch(core_types.models.Choice):
    class Meta:
        verbose_name = _('Court And Branch')
        verbose_name_plural = _('Courts And Branches')
