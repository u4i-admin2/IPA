"""
Editable types
"""

from django.db import models
from django.db.models.signals import (
    post_save,
    post_delete
)
from django.utils.translation import ugettext_lazy as _

from ipa.models import CsvState
from .signals import update_activities
from core_types.models import (
    City,
    Province,
    Religion,
    Ethnicity,
    Country,
    PublishableMixin,
    Quote,
    File,
    Comment,
    Source,
    Timeline,
    Choice
)
from core_types.managers import PublishedManager
from judges.models import (
    Judge,
    CourtAndBranch,
    SentenceType,
    BehaviourType
)
from prisons.models import Prison
from core_types.fields import PartialDateField


class DetentionStatus(Choice):
    """
    Which international laws were violated?
    """
    detained = models.BooleanField(
        default=True,
        verbose_name=_('Prisoner is currently in detention'),
        help_text=_('When this status is selected, should the prisoner '
                    'be considered as currently incarcerated? This '
                    'affects list view filtering.'))

    class Meta:
        verbose_name = _('Detention Status')
        verbose_name_plural = _('Detention Statuses')


class Prisoner(PublishableMixin, models.Model):
    forename = models.CharField(
        verbose_name=_('First Name'),
        max_length=255,
        null=True,
        blank=True)

    surname = models.CharField(
        verbose_name=_('Surname'),
        max_length=255)

    GENDER = [('M', _('Male')),
              ('F', _('Female'))]

    gender = models.CharField(
        verbose_name=_('Gender'),
        max_length=1,
        choices=GENDER,
        null=True,
        blank=True)

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

    birth_city = models.ForeignKey(
        City,
        verbose_name=_('Birth Village/City'),
        null=True,
        blank=True)

    birth_province = models.ForeignKey(
        Province,
        verbose_name=_('Birth Province'),
        null=True,
        blank=True)

    religion = models.ForeignKey(
        Religion,
        verbose_name=_('Religion'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    ethnicity = models.ForeignKey(
        Ethnicity,
        verbose_name=_('Ethnicity'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    picture = models.ImageField(
        verbose_name=_('Prisoner Picture'),
        upload_to='prisoner_pics',
        null=True,
        blank=True)

    detention_status = models.ForeignKey(
        DetentionStatus,
        verbose_name=_('Detention Status'),
        null=True,
        blank=True)

    needs_attention = models.BooleanField(
        verbose_name=_('Needs attention'),
        default=False)

    home_countries = models.ManyToManyField(
        Country,
        verbose_name=_('Countries Of Residence'),
        blank=True)

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

    detention_is_approx = models.BooleanField(
        verbose_name=_('Detention date is approximate?'),
        default=False)

    #
    # The following fields are cached at save time to avoid turning search
    # results rendering into a huge number of SELECT * ORDER BY -date queries.
    # We populate/remove them using a signal to ensure every update/delete is
    # accounted for.
    #

    latest_activity_persecuted_for_name_en = models.TextField(
        verbose_name=_('Most recent activity (cached for search results)'),
        null=True,
        blank=True)

    latest_activity_persecuted_for_name_fa = models.TextField(
        verbose_name=_('Most recent activity (cached for search results)'),
        null=True,
        blank=True)

    latest_secondary_activity_name_en = models.TextField(
        verbose_name=_('Most recent secondary activity (cached for search results)'),
        null=True,
        blank=True)

    latest_secondary_activity_name_fa = models.TextField(
        verbose_name=_('Most recent secondary activity (cached for search results)'),
        null=True,
        blank=True)

    latest_tertiary_activity_name_en = models.TextField(
        verbose_name=_('Most recent tertiary activity (cached for search results)'),
        null=True,
        blank=True)

    latest_tertiary_activity_name_fa = models.TextField(
        verbose_name=_('Most recent tertiary activity (cached for search results)'),
        null=True,
        blank=True)

    latest_detention_status_name_en = models.TextField(
        verbose_name=_('Most recent sentence of most recent '
                       'arrrest, if any (cached for search results)'),
        null=True,
        blank=True)

    latest_prison_name_en = models.TextField(
        verbose_name=_('Prison of most recent detention of '
                       'most recent arrest (cached for search results)'),
        null=True,
        blank=True)

    latest_sentenced_judge_name_en = models.TextField(
        verbose_name=_('Judge name of most recent sentence of '
                       'most recent arrest (cached for search results)'),
        null=True,
        blank=True)

    latest_sentenced_judge_name_fa = models.TextField(
        verbose_name=_('Judge name of most recent sentence of '
                       'most recent arrest (cached for search results)'),
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

    featured = models.BooleanField(
        default=False)

    _is_updating_cache_fields = False

    def get_arrest(self, number):
        """
        Return number-th last arrest:
            number = 1: last arrest
            number = 2: second last arrest
            ...
        """
        if number < 1:
            return None

        arrest = (PrisonerArrest.objects
                  .filter(prisoner=self)
                  .order_by('-arrest_year', '-arrest_month', '-arrest_day'))
        if number > arrest.count():
            return None

        return arrest[number - 1]

    def get_judges_involved(self, arrest):
        """
        returns all judges involved with this prisoner
        """
        sentences = PrisonerSentence.objects.filter(arrest=arrest)
        judges = Judge.objects.filter(sentences__in=sentences).distinct()

        return judges if judges.count() > 0 else None

    def get_sentence_behaviours(self, arrest):
        """
        Returns all behaviours involved with this arrest
        """
        sentences = PrisonerSentence.objects.filter(arrest=arrest)
        behaviours = SentenceBehaviour.objects.filter(sentence__in=sentences).distinct()

        return behaviours if behaviours.count() > 0 else None

    def update_summary_fields(self):
        """
        When some related arrest/sentence/detention has changed, run a bunch of
        expensive queries and cache their result for use by the Watson
        api/search.py viewset / PrisonerSummarySerializer.
        """
        if self._is_updating_cache_fields:
            return

        arrest = (PrisonerArrest.objects
                  .filter(prisoner=self)
                  .order_by('-arrest_year', '-arrest_month', '-arrest_day')
                  .first())
        self.latest_activity_persecuted_for_name_en = (
            arrest.activity_persecuted_for.name_en
            if (arrest and arrest.activity_persecuted_for)
            else None)
        self.latest_activity_persecuted_for_name_fa = (
            arrest.activity_persecuted_for.name_fa
            if (arrest and arrest.activity_persecuted_for)
            else None)

        self.latest_secondary_activity_name_en = (
            arrest.secondary_activity.name_en
            if (arrest and arrest.secondary_activity)
            else None)
        self.latest_secondary_activity_name_fa = (
            arrest.secondary_activity.name_fa
            if (arrest and arrest.secondary_activity)
            else None)

        self.latest_tertiary_activity_name_en = (
            arrest.tertiary_activity.name_en
            if (arrest and arrest.tertiary_activity)
            else None)
        self.latest_tertiary_activity_name_fa = (
            arrest.tertiary_activity.name_fa
            if (arrest and arrest.tertiary_activity)
            else None)

        self.latest_detention_status_name_en = (
            self.detention_status.name_en
            if self.detention_status
            else None)

        sentence = (PrisonerSentence.objects
                    .filter(arrest=arrest)
                    .order_by('-sentence_type__finality', '-id')
                    .first())

        self.latest_sentenced_judge_name_en = (
            sentence.judge.surname_en
            if sentence and sentence.judge
            else None)
        self.latest_sentenced_judge_name_fa = (
            sentence.judge.surname_fa
            if sentence and sentence.judge
            else None)

        detention = (PrisonerDetention.objects
                     .filter(arrest=arrest)
                     .order_by('-detention_year', '-detention_month', '-detention_day')
                     .first())
        self.latest_prison_name_en = (
            detention.prison.name_en
            if detention and detention.prison
            else None)

        self._is_updating_cache_fields = True
        self.save()
        self._is_updating_cache_fields = False

    def _on_related_save(sender, instance, raw=None, **kwargs):
        """
        Watch saves/deletes to prisoners/arrests/sentences/detentions and
        update cached search results fields as necessary.
        """
        if raw:
            return

        if isinstance(instance, Prisoner):
            instance.refresh_from_db()
            instance.update_summary_fields()
        elif isinstance(instance, PrisonerArrest):
            instance.prisoner.update_summary_fields()
        elif isinstance(instance, PrisonerSentence):
            instance.arrest.prisoner.update_summary_fields()
        elif isinstance(instance, PrisonerDetention):
            instance.arrest.prisoner.update_summary_fields()

    def _on_related_delete(sender, instance, raw=None, **kwargs):
        """
        Watch saves/deletes to prisoners/arrests/sentences/detentions and
        update cached search results fields as necessary.
        """
        if isinstance(instance, PrisonerArrest):
            instance.prisoner.update_summary_fields()
        elif isinstance(instance, PrisonerSentence):
            instance.arrest.prisoner.update_summary_fields()
        elif isinstance(instance, PrisonerDetention):
            instance.arrest.prisoner.update_summary_fields()

    def _set_csv_dirty(sender, instance, raw=None, **kwargs):
        """
        if prisoners changed we need to write CSV file again
        """
        if raw:
            return

        if (not isinstance(instance, Prisoner) and
                not isinstance(instance, PrisonerArrest) and
                not isinstance(instance, PrisonerSentence) and
                not isinstance(instance, PrisonerDetention)):
            return

        try:
            csvstate = CsvState.objects.first()
        except CsvState.DoesNotExist:
            csvstate.objects.create(
                should_write_csv=True)
            return

        if csvstate is None:
            csvstate.objects.create(
                should_write_csv=True)
        else:
            csvstate.should_write_csv = True
            csvstate.save()

    def get_name(self):
        first = self.forename or ''
        second = self.surname or ''
        name = "%s %s" % (first, second)
        return name.strip()

    post_save.connect(_on_related_save)
    post_delete.connect(_on_related_delete)
    post_save.connect(_set_csv_dirty)
    post_delete.connect(_set_csv_dirty)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        verbose_name = _('Prisoner')
        verbose_name_plural = _('Prisoners')

    def __unicode__(self):
        return u'%s %s: %s %s' % (
            type(self).__name__,
            self.pk,
            self.forename,
            self.surname)

    @classmethod
    def prefetch_queryset(cls, queryset):
        """
        Update a queryset to prefetch all related data for a prisoner.
        """
        return (
            queryset
            .select_related('created_by')
            .select_related('updated_by')
            .prefetch_related('quotes')
            .prefetch_related('files')
            .prefetch_related('home_countries')
            .prefetch_related('timeline')
            .prefetch_related('sources')
            .prefetch_related('affiliations')
            .prefetch_related('affiliations__organisation')
            .prefetch_related('affiliations__relationship_type')
            .prefetch_related('relationships')
            .prefetch_related('relationships__relationship_type')
            .select_related('religion')
            .select_related('detention_status')
            .prefetch_related('comments')
            .select_related('ethnicity')
            .select_related('birth_city')
            .select_related('birth_province')
            .prefetch_related('arrests')
            .prefetch_related('arrests__activity_persecuted_for')
            .prefetch_related('arrests__secondary_activity')
            .prefetch_related('arrests__tertiary_activity')
            .prefetch_related('arrests__case_id')
            .prefetch_related('arrests__charged_with')
            .prefetch_related('arrests__city')
            .prefetch_related('arrests__domestic_law_violated')
            .prefetch_related('arrests__international_law_violated')
            .prefetch_related('arrests__province')
            .prefetch_related('arrests__sentences')
            .prefetch_related('arrests__sentences__court_and_branch')
            .prefetch_related('arrests__sentences__judge')
            .prefetch_related('arrests__sentences__behaviours')
            .prefetch_related('arrests__sentences__behaviours__behaviour_type')
            .prefetch_related('arrests__sentences__sentence_type')
            .prefetch_related('arrests__detentions')
            .prefetch_related('arrests__detentions__prison')
            .prefetch_related('arrests__detentions__treatment'))


class PrisonerQuote(Quote):
    prisoner = models.ForeignKey(
        Prisoner,
        related_name='quotes')


class PrisonerFile(File):
    prisoner = models.ForeignKey(
        Prisoner,
        related_name='files')

    FILE_TYPE_CHOICES = [
        ('prisoner_activism', _('Prisoner\'s activism')),
        ('court', _('Court')),
        ('media', _('Media')),
        ('family', _('Family')),
        ('campaigns', _('Campaigns')),
    ]

    file_type = models.CharField(
        choices=FILE_TYPE_CHOICES,
        max_length=20,
    )


class PrisonerComment(Comment):
    prisoner = models.ForeignKey(
        Prisoner,
        related_name='comments')


class PrisonerSource(Source):
    prisoner = models.ForeignKey(
        Prisoner,
        related_name='sources')

    class Meta:
        unique_together = [
            ('prisoner', 'name'),
        ]


class RelationshipType(Choice):
    """
    Describes the nature of the relationship between prisoners and
    organisations.
    """
    class Meta:
        verbose_name = _('Relationship Type')


class PrisonerRelationship(PublishableMixin, models.Model):
    prisoner = models.ForeignKey(
        Prisoner,
        related_name='relationships')

    forename = models.CharField(
        verbose_name=_('First Name'),
        max_length=255,
        null=True,
        blank=True)

    surname = models.CharField(
        verbose_name=_('Surname'),
        max_length=255,
        null=True,
        blank=True)

    relationship_type = models.ForeignKey(
        RelationshipType,
        verbose_name=_('Type'))

    related_prisoner = models.ForeignKey(
        Prisoner,
        related_name='+',
        null=True,
        blank=True)

    is_confirmed = models.BooleanField(
        verbose_name=_('Alleged or confirmed?'),
        default=False)

    class Meta:
        verbose_name = _('Relationship')

    def __unicode__(self):
        return u'%s %s' % (type(self).__name__, self.pk)


class Organisation(Choice):
    """
    Organisation the prisoner is affiliated with.
    """
    class Meta:
        verbose_name = _('Affiliated Organization')


class PrisonerAffiliation(PublishableMixin, models.Model):
    prisoner = models.ForeignKey(
        Prisoner,
        related_name='affiliations')

    organisation = models.ForeignKey(
        Organisation)

    relationship_type = models.ForeignKey(
        RelationshipType)

    confirmed = models.BooleanField(
        default=False)

    class Meta:
        verbose_name = _('Affiliation')

    def __unicode__(self):
        return u'%s %s' % (type(self).__name__, self.pk)


class ActivityPersecutedFor(Choice):
    """
    Ie blogger, journalist etc.
    """
    class Meta:
        verbose_name = _('Persecuted Activity')
        verbose_name_plural = _('Persecuted Activities')

    # def save(self, *args, **kwargs):
    #     super(self, ActivityPersecutedFor).save(*args, **kwargs)
    #     arrests = PrisonerArrest.objects.filter(
    #         activity_persecuted_for=self)
    #     for arrest in arrests:
    #         arrest.prisoner.update_summary_fields()


post_save.connect(update_activities, sender=ActivityPersecutedFor)


class CaseId(Choice):
    """
    Research should be able to add a case with unique identifying features so
    that prisoners who have been charged on the same case would be linked.
    """
    class Meta:
        verbose_name = _('Case ID')
        verbose_name_plural = _('Case IDs')


class PrisonerArrest(PublishableMixin, models.Model):
    """
    A prisoner can have multiple 'arrest details' filed against their name. The
    default display will be the most recent. Others will be archived.
    """
    partial_date = PartialDateField(null=True, blank=True)

    prisoner = models.ForeignKey(
        Prisoner,
        related_name='arrests')

    arrest_year = models.IntegerField(
        verbose_name=_('Arrest Year (Gregorian)'),
        null=True,
        blank=True)

    arrest_month = models.IntegerField(
        verbose_name=_('Arrest Month (Gregorian)'),
        null=True,
        blank=True)

    arrest_day = models.IntegerField(
        verbose_name=_('Arrest Day (Gregorian)'),
        null=True,
        blank=True)

    arrest_year_fa = models.IntegerField(
        verbose_name=_('Arrest Year (Persian)'),
        null=True,
        blank=True)

    arrest_month_fa = models.IntegerField(
        verbose_name=_('Arrest Month (Persian)'),
        null=True,
        blank=True)

    arrest_day_fa = models.IntegerField(
        verbose_name=_('Arrest Day (Persian)'),
        null=True,
        blank=True)

    activity_persecuted_for = models.ForeignKey(
        ActivityPersecutedFor,
        verbose_name=_('Activity Persecuted For'),
        null=True,
        blank=True)

    secondary_activity = models.ForeignKey(
        ActivityPersecutedFor,
        verbose_name=_('Secondary Activity'),
        null=True,
        blank=True,
        related_name='secondary_activity')

    tertiary_activity = models.ForeignKey(
        ActivityPersecutedFor,
        verbose_name=_('Tertiary Activity'),
        null=True,
        blank=True,
        related_name='tertiary_activity')

    city = models.ForeignKey(
        City,
        verbose_name=_('City of arrest'),
        null=True,
        blank=True)

    case_id = models.ForeignKey(
        CaseId,
        verbose_name=_('Case ID'),
        null=True,
        blank=True)

    # sometimes they don't know the city...
    province = models.ForeignKey(
        Province,
        verbose_name=_('Province of arrest'),
        null=True,
        blank=True)

    charged_with = models.ManyToManyField(
        'ChargedWith',
        verbose_name=_('Charged with'),
        blank=True)

    domestic_law_violated = models.ManyToManyField(
        'DomesticLawViolated',
        verbose_name=_('Domestic Law Violated'),
        blank=True)

    international_law_violated = models.ManyToManyField(
        'InternationalLawViolated',
        verbose_name=_('International law violated'),
        blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        verbose_name = _('Arrest')
        ordering = ('arrest_year', 'arrest_month', 'arrest_day')

    def __unicode__(self):
        return u'%s %s' % (type(self).__name__, self.pk)

    def has_death_penalty(self):
        return self.sentences.first().death_penalty if self.sentences.count() > 0 else False

    def has_life(self):
        return self.sentences.first().life if self.sentences.count() > 0 else False

    def has_exile(self):
        return self.sentences.first().exiled if self.sentences.count() > 0 else False

    def number_of_years(self):
        return self.sentences.first().sentence_years \
            if self.sentences.count() > 0 and self.sentences.first().sentence_years else 0

    def number_of_months(self):
        return self.sentences.first().sentence_months \
            if self.sentences.count() > 0 and self.sentences.first().sentence_months else 0

    def total_fine(self):
        return self.sentences.first().fine \
            if self.sentences.count() > 0 and self.sentences.first().fine else 0

    def number_of_lashes(self):
        return self.sentences.first().number_of_lashes \
            if self.sentences.count() > 0 and self.sentences.first().number_of_lashes else 0

    def social_depravations(self):
        return self.sentences.first().social_depravation \
            if self.sentences.count() > 0 and self.sentences.first().social_depravation else ''

    def save(self, *args, **kwargs):
        if self.arrest_year:
            partial_date = '{0:04}'.format(self.arrest_year)
            if self.arrest_month:
                partial_date += '-{0:02}'.format(self.arrest_month)
                if self.arrest_day:
                    partial_date += '-{0:02}'.format(self.arrest_day)
            self.partial_date = partial_date
        super(PrisonerArrest, self).save(*args, **kwargs)


class PrisonTreatment(Choice):
    class Meta:
        verbose_name = _('Treatment In Prison')
        verbose_name_plural = _('Treatment In Prison')


class PrisonerDetention(PublishableMixin, models.Model):
    """
    An individual's sentence might have multiple prison details. Sometimes a
    prisoner is detained in a prison after arrest and transferred to a
    different prison after sentencing. Sometimes a prisoner is transferred
    during a sentence too. Each of these should be able to have a separate
    record. We would display by default the current.
    """
    arrest = models.ForeignKey(
        PrisonerArrest,
        related_name='detentions')

    prison = models.ForeignKey(
        Prison,
        verbose_name=_('Prison'),
        related_name='detentions',
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

    treatment = models.ManyToManyField(
        PrisonTreatment,
        verbose_name=_('Treatment in prison'),
        blank=True)

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
        super(PrisonerDetention, self).save(*args, **kwargs)

        if self.is_published:
            if self.arrest and self.arrest.is_published:
                for sentence in self.arrest.sentences.filter(is_published=True):
                    if sentence.judge:
                        sentence.judge.update_mistreatment()


class PrisonerSentence(PublishableMixin, models.Model):
    """
    For each instance of arrest, a prisoner might encounter multiple judges
    during the different phases of their arrest and receive differing sentence
    lengths.

    For the purposes of presenting data, we will use the highest level of
    sentencing (eg Supreme) to count towards the cumulative total.
    """
    arrest = models.ForeignKey(
        PrisonerArrest,
        related_name='sentences')

    judge = models.ForeignKey(
        Judge,
        verbose_name=_('Judge'),
        related_name='sentences',
        null=True,
        blank=True)

    # sometimes they don't know the judge and only have the court...
    court_and_branch = models.ForeignKey(
        CourtAndBranch,
        verbose_name=_('Court'),
        null=True,
        blank=True)

    death_penalty = models.BooleanField(
        verbose_name=_('Death Penalty'),
        default=False)

    exiled = models.BooleanField(
        verbose_name=_('Exiled'),
        default=False)

    life = models.BooleanField(
        verbose_name=_('Life'),
        default=False)

    social_depravation = models.TextField(
        verbose_name=_('Social Deprivation'),
        null=True,
        blank=True)

    fine = models.BigIntegerField(
        verbose_name=_('Fine (Rials)'),
        null=True,
        blank=True)

    number_of_lashes = models.PositiveIntegerField(
        verbose_name=_('Number Of Lashes'),
        null=True,
        blank=True)

    sentence_months = models.PositiveIntegerField(
        verbose_name=_('Sentence Months'),
        null=True,
        blank=True)

    sentence_years = models.PositiveIntegerField(
        verbose_name=_('Sentence Years'),
        null=True,
        blank=True)

    sentence_type = models.ManyToManyField(
        SentenceType,
        verbose_name=_('Type'),
        blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        verbose_name = _('Sentence')
        ordering = ('-sentence_type__finality', '-id')

    def __unicode__(self):
        return u'%s %s' % (type(self).__name__, self.pk)


class SentenceBehaviour(PublishableMixin, models.Model):
    sentence = models.ForeignKey(
        PrisonerSentence,
        related_name='behaviours')

    behaviour_type = models.ForeignKey(
        BehaviourType,
        verbose_name=_('Type'),
        related_name='+')

    description = models.TextField(
        verbose_name=_('Description of Behaviour'),
        null=True,
        blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        verbose_name = _('Sentence Judicial Behaviour')


class PrisonerTimeline(Timeline):
    prisoner = models.ForeignKey(
        Prisoner,
        related_name='timeline')


class ChargedWith(Choice):
    """
    What were they charged with?
    """
    class Meta:
        verbose_name = _('Charged With')


class DomesticLawViolated(Choice):
    """
    Which domestic laws were violated?
    """
    class Meta:
        verbose_name = _('Domestic Law Violated')
        verbose_name_plural = _('Domestic Law Violated')


class InternationalLawViolated(Choice):
    """
    Which international laws were violated?
    """
    class Meta:
        verbose_name = _('International Law Violated')
        verbose_name_plural = _('International Law Violated')
