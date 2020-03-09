# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from prisoners.models import (
    InternationalLawViolated,
    DomesticLawViolated,
    PrisonTreatment
)
from judges.models import (
    Judge,
    BehaviourType,
    CourtAndBranch
)
from core_types.models import (
    City,
    PublishablePublishedByDefaultModel,
    File,
    Comment,
    Quote,
    Choice
)
from core_types.managers import PublishedManager
from core_types.fields import PartialDateField
from prisons.models import Prison


class HumanRightViolated(Choice):
    class Meta:
        verbose_name = _('Human Right Violated')
        verbose_name_plural = _('Human Right Violated')


class ReportChargedWith(Choice):
    """
    What were they charged with?
    """
    class Meta:
        verbose_name = _('Charged With')


class Report(PublishablePublishedByDefaultModel):
    picture = models.ImageField(
        verbose_name=_('Report Picture'),
        upload_to='report_pics',
        null=True,
        blank=True)

    abstract_text = models.TextField(
        null=True,
        blank=True)

    abstract_text_en = models.TextField(
        null=True,
        blank=True)

    abstract_text_fa = models.TextField(
        null=True,
        blank=True)

    victim_count = models.IntegerField(
        verbose_name=_('Number of victims in the report'),
        null=True,
        blank=True)

    city = models.ForeignKey(
        City,
        verbose_name=_('City of arrest'),
        null=True,
        blank=True)

    charged_with = models.ManyToManyField(
        ReportChargedWith,
        verbose_name=_('Charged with'),
        blank=True)

    domestic_law_violated = models.ManyToManyField(
        DomesticLawViolated,
        verbose_name=_('Domestic Law Violated'),
        blank=True)

    international_law_violated = models.ManyToManyField(
        InternationalLawViolated,
        verbose_name=_('International law violated'),
        blank=True)

    human_right_violated = models.ManyToManyField(
        HumanRightViolated,
        verbose_name=_('Human Rights violated'),
        blank=True)

    partial_date = PartialDateField(null=True, blank=True)

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

    objects = models.Manager()
    published_objects = PublishedManager()

    def __unicode__(self):
        return "{} - {} victims".format(self.abstract_text_fa, unicode(self.victim_count))

    # def save(self, *args, **kwargs):
    #     if self.detention_year:
    #         partial_date = '{0:04}'.format(self.detention_year)
    #         if self.detention_month:
    #             partial_date += '-{0:02}'.format(self.detention_month)
    #             if self.detention_day:
    #                 partial_date += '-{0:02}'.format(self.detention_day)
    #         self.partial_date = partial_date

    #     super(Report, self).save(*args, **kwargs)


class ReportFile(File):
    # This overrides the is_published field of PublishableMixin, which
    # is inherited by File.
    is_published = models.BooleanField(
        verbose_name=_('Approved for publishing?'),
        db_index=True,
        default=True)

    report = models.ForeignKey(
        Report,
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


class ReportSentence(PublishablePublishedByDefaultModel):
    execution = models.BooleanField(
        default=False)
    flogging = models.BooleanField(
        default=False)
    amputation = models.BooleanField(
        default=False)
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='sentences')
    judge = models.ForeignKey(
        Judge,
        on_delete=models.SET_NULL,
        related_name='report_sentences',
        null=True,
        blank=True)
    # sometimes they don't know the judge and only have the court...
    judge_court_and_branch = models.ForeignKey(
        CourtAndBranch,
        on_delete=models.SET_NULL,
        related_name='report_sentences',
        null=True,
        blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()

    def __unicode__(self):
        return "{} by {}".format(self.report, self.judge)

    class Meta:
        verbose_name = _('Report Sentence')
        verbose_name_plural = _('Report Sentences')


class ReportComment(Comment):
    report = models.ForeignKey(
        Report,
        related_name='comments')


class ReportQuote(Quote):
    # This overrides the is_published field of PublishableMixin, which
    # is inherited by Quote.
    is_published = models.BooleanField(
        verbose_name=_('Approved for publishing?'),
        db_index=True,
        default=True)

    prison = models.ForeignKey(
        Report,
        related_name='quotes')


class ReportSource(PublishablePublishedByDefaultModel):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='sources')

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True)

    link = models.CharField(
        max_length=1024,
        null=True,
        blank=True)

    description = models.TextField(
        null=True,
        blank=True)

    related_fields = models.TextField(
        null=True,
        blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()


class ReportDetention(PublishablePublishedByDefaultModel):
    report = models.ForeignKey(
        Report,
        related_name='detentions')

    prison = models.ForeignKey(
        Prison,
        verbose_name=_('Prison'),
        related_name='report_detentions',
        null=True,
        blank=True)

    DETENTION_TYPE_CHOICES = [
        ('detained_before_sentencing', _('Detained before Sentencing')),
        ('sentenced', _('Sentenced')),
        ('transferred', _('Transferred')),
    ]

    detention_type = models.CharField(
        verbose_name=_('Detention Type'),
        choices=DETENTION_TYPE_CHOICES,
        null=True,
        blank=True,
        max_length=255)

    detention_year = models.IntegerField(
        verbose_name=_('Detention Year (Gregorian)'),
        null=True,
        blank=True)

    detention_month = models.IntegerField(
        verbose_name=_('Detention Month (Gregorian)'),
        null=True,
        blank=True)

    detention_day = models.IntegerField(
        verbose_name=_('Detention Day (Gregorian)'),
        null=True,
        blank=True)

    detention_year_fa = models.IntegerField(
        verbose_name=_('Detention Year (Persian)'),
        null=True,
        blank=True)

    detention_month_fa = models.IntegerField(
        verbose_name=_('Detention Month (Persian)'),
        null=True,
        blank=True)

    detention_day_fa = models.IntegerField(
        verbose_name=_('Detention Day (Persian)'),
        null=True,
        blank=True)

    treatment = models.ManyToManyField(
        PrisonTreatment,
        verbose_name=_('Treatment in prison'),
        blank=True)

    detention_is_approx = models.BooleanField(
        verbose_name=_('Detention date is approximate?'),
        default=False)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        verbose_name = _('Detention')
        ordering = ('-id',)

    def __unicode__(self):
        return u'%s %s' % (type(self).__name__, self.pk)

    def save(self, *args, **kwargs):
        super(ReportDetention, self).save(*args, **kwargs)

        if self.is_published:
            if self.report and self.report.is_published:
                for sentence in self.report.sentences.filter(is_published=True):
                    if sentence.judge:
                        sentence.judge.update_mistreatment()


class ReportSentenceBehaviour(PublishablePublishedByDefaultModel):
    description = models.TextField(
        null=True,
        blank=True)

    description_fa = models.TextField(
        null=True,
        blank=True)

    description_en = models.TextField(
        null=True,
        blank=True)

    judge_behaviour = models.ForeignKey(
        BehaviourType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sentence_behaviours')

    report_sentence = models.ForeignKey(
        ReportSentence,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sentence_behaviours')

    objects = models.Manager()
    published_objects = PublishedManager()
