from __future__ import division

from datetime import date
from collections import defaultdict

from django.utils.translation import ugettext as _
from django.db.models import Count, Sum

import rest_framework.serializers

import api.fields
import core_types
import logging
import judges
import prisoners.models
import prisons
import public.utils
import report

from report.models import (
    ReportDetention,
    ReportSentence,
)


logger = logging.getLogger(__name__)


class PrisonerArrestSummarySerializer(prisoners.serializers.PrisonerArrestSerializer):
    """ Used on the judge page, prison page to deliver a query-lite prisoner for ajax gets """
    class Meta:
        model = prisoners.models.PrisonerArrest
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'prisoner_id',
            'arrest_year',
            'arrest_month',
            'arrest_day',
            'arrest_year_fa',
            'arrest_month_fa',
            'arrest_day_fa',
            'activity_persecuted_for',
            'charged_with_objs',
            'sentences',
        )


class PrisonerStatusSummary(prisoners.serializers.PrisonerSerializer):
    """ Used on the judge page, prison page to deliver a query-lite prisoner for ajax gets """
    arrests = PrisonerArrestSummarySerializer(
        many=True,
        read_only=True)

    class Meta:
        model = prisoners.models.Prisoner
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'forename',
            'surname',
            'picture_resized',
            'arrests'
        )


class ReportStatusSummary(report.serializers.ReportSerializer):
    """ Used on the judge page, prison page to deliver a query-lite prisoner for ajax gets """

    domestic_law_violated = report.serializers.DomesticLawViolatedSerializer(
        many=True,
        read_only=True)

    international_law_violated = report.serializers.InternationalLawViolatedSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = report.models.Report
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'city',
            'picture',
            'victim_count',
            'domestic_law_violated',
            'international_law_violated',
        )


"""
The search pages uses these bespoke serializer
"""


class SearchPageJudgeSerializer(core_types.serializers.PublishableModelSerializer):
    """
    Court and branch
    Age range
    Judge type 1: Cleric/ Not cleric/ Unknown
    Judge type 2: Research/ Primary/ Appeal/ Supreme
    Position
    Additional Evidence: Have / Have not
    """
    age = rest_framework.serializers.SerializerMethodField()
    files = rest_framework.serializers.SerializerMethodField()
    quotes = rest_framework.serializers.SerializerMethodField()
    name = rest_framework.serializers.SerializerMethodField()
    judge_type_secondary = rest_framework.serializers.SerializerMethodField()
    court_and_branch = rest_framework.serializers.ReadOnlyField(
        source='court_and_branch.name')
    is_cleric = rest_framework.serializers.SerializerMethodField()

    picture_200x200 = api.fields.ThumbnailImageField(source='picture', size=(200, 200))

    total_verdicts = rest_framework.serializers.SerializerMethodField()
    average_sentence = rest_framework.serializers.SerializerMethodField()

    def get_judge_type_secondary(self, obj):
        positions = []
        if obj.judicial_position:
            positions.append(obj.judicial_position.name)
        pos_objs = obj.positions.all()
        for pos_obj in pos_objs:
            if pos_obj.judicial_position:
                positions.append(pos_obj.judicial_position.name)
        return set(positions)

    def get_name(self, obj):
        first = obj.forename or ''
        second = obj.surname or ''
        name = "%s %s" % (first, second)
        return name.strip()

    def get_age(self, obj):
        if obj.dob_year:
            month = obj.dob_month or 1
            day = obj.dob_day or 1
            return public.utils.calculate_age(
                date(obj.dob_year, month, day))
        return 0

    def get_is_cleric(self, obj):
        if obj.is_cleric is None:
            is_cleric = _('Unknown')
        else:
            is_cleric = obj.is_cleric
        return unicode(is_cleric)

    def get_files(self, obj):
        return bool(obj.files.all())

    def get_quotes(self, obj):
        return bool(obj.quotes.all())

    def query_sentences(self, obj):
        recreate = False
        if getattr(self, 'sentence_stats', None) and self.sentence_stats['current_obj'] != obj.id:
            recreate = True

        if not getattr(self, 'sentence_stats', None) or recreate:
            self.sentence_stats = obj.sentences.aggregate(
                total_years=Sum('sentence_years'),
                total_verdicts=Count('id'))
            self.sentence_stats['current_obj'] = obj.id

        return self.sentence_stats

    def get_total_verdicts(self, obj):
        return self.query_sentences(obj)['total_verdicts']

    def get_average_sentence(self, obj):
        stats = self.query_sentences(obj)
        result = 0
        try:
            result = round((stats['total_years'] or 0) / (stats['total_verdicts'] or 0), 1)
        except ZeroDivisionError:
            pass
        return result

    class Meta:
        model = judges.models.Judge
        fields = core_types.serializers.PUBLISHABLE_READ_ONLY_FIELDS + (
            'id',
            'age',
            'files',
            'quotes',
            'name',
            'judge_type',
            'judge_type_secondary',
            'is_cleric',
            'court_and_branch',
            'picture_200x200',
            'total_verdicts',
            'average_sentence',
        )


class AeaSearchPageJudgeSerializer(SearchPageJudgeSerializer):
    total_victim_count = rest_framework.serializers.SerializerMethodField()

    def get_total_victim_count(self, obj):
        aggregates_dict = (
            ReportSentence
            .published_objects
            .filter(
                judge=obj
            )
            .aggregate(
                total_victims=Sum('report__victim_count')
            )
        )

        return aggregates_dict['total_victims']

    class Meta:
        model = judges.models.Judge
        fields = core_types.serializers.PUBLISHABLE_READ_ONLY_FIELDS + (
            'id',
            'age',
            'files',
            'quotes',
            'name',
            'judge_type',
            'judge_type_secondary',
            'is_cleric',
            'court_and_branch',
            'picture_200x200',
            'total_victim_count',
        )


class SearchPagePrisonSerializer(core_types.serializers.PublishableModelSerializer):

    facilities = rest_framework.serializers.SerializerMethodField()
    quotes = rest_framework.serializers.SerializerMethodField()
    files = rest_framework.serializers.SerializerMethodField()
    treatments = rest_framework.serializers.SerializerMethodField()
    activities = rest_framework.serializers.SerializerMethodField()
    capacity = rest_framework.serializers.SerializerMethodField()
    prisoners_incarcerated = rest_framework.serializers.SerializerMethodField()

    picture_200x200 = api.fields.ThumbnailImageField(source='picture', size=(200, 200))

    def get_facilities(self, obj):
        facilities = obj.facilities.all()
        return [facility.name for facility in facilities]

    def get_files(self, obj):
        return bool(obj.files.all())

    def get_quotes(self, obj):
        return bool(obj.quotes.all())

    def get_treatments(self, obj):
        detentions = obj.detentions.all()
        prison_treatments = []
        for detention in detentions:
            prison_treatments += [treatment.name for treatment in detention.treatment.all()]
        return set(prison_treatments)

    def get_activities(self, obj):
        detentions = obj.detentions.all()
        activities = []
        for detention in detentions:
            if detention.arrest.activity_persecuted_for:
                activities.append(detention.arrest.activity_persecuted_for.name)
        return set(activities)

    def get_prisoners_incarcerated(self, obj):
        return obj.detentions.all().count()

    def get_capacity(self, obj):
        capacity = 0
        if obj.capacity:
            capacity = obj.capacity
        return capacity

    class Meta:
        model = prisons.models.Prison
        fields = core_types.serializers.PUBLISHABLE_READ_ONLY_FIELDS + (
            'id',
            'name',
            'capacity',
            'facilities',
            'quotes',
            'files',
            'picture_200x200',
            'treatments',
            'activities',
            'administered_by',
            'prisoners_incarcerated'
        )


class AeaSearchPagePrisonSerializer(SearchPagePrisonSerializer):
    total_victim_count = rest_framework.serializers.SerializerMethodField()

    def get_total_victim_count(self, obj):
        aggregates_dict = (
            ReportDetention
            .published_objects
            .filter(
                prison=obj
            )
            .aggregate(
                total_victims=Sum('report__victim_count')
            )
        )

        return aggregates_dict['total_victims']

    class Meta:
        model = prisons.models.Prison
        fields = core_types.serializers.PUBLISHABLE_READ_ONLY_FIELDS + (
            'id',
            'name',
            'capacity',
            'facilities',
            'quotes',
            'files',
            'picture_200x200',
            'treatments',
            'activities',
            'administered_by',
            'total_victim_count',
        )


class SearchPagePrisonerSerializer(core_types.serializers.PublishableModelSerializer):

    files = rest_framework.serializers.SerializerMethodField()
    quotes = rest_framework.serializers.SerializerMethodField()
    affiliations = rest_framework.serializers.SerializerMethodField()

    name = rest_framework.serializers.SerializerMethodField()

    religion = rest_framework.serializers.ReadOnlyField(source='religion.name')
    ethnicity = rest_framework.serializers.ReadOnlyField(source='ethnicity.name')
    detention_status = rest_framework.serializers.ReadOnlyField(source='detention_status.detained')

    picture_200x200 = api.fields.ThumbnailImageField(source='picture', size=(200, 200))
    age = rest_framework.serializers.SerializerMethodField()

    # aggregate all activites and charges across all arrests
    all_arrests_activities = rest_framework.serializers.SerializerMethodField()
    all_arrests_charges = rest_framework.serializers.SerializerMethodField()

    # aggregate all prisons from detentions
    all_arrests_prisons = rest_framework.serializers.SerializerMethodField()
    # aggregate all treatments from detentions
    all_arrests_prison_treatments = rest_framework.serializers.SerializerMethodField()

    # aggregate all sentences
    # all_arrests_sentences = rest_framework.serializers.SerializerMethodField()
    all_sentences_judges = rest_framework.serializers.SerializerMethodField()
    all_sentences_death_penalty = rest_framework.serializers.SerializerMethodField()
    all_sentences_exiled = rest_framework.serializers.SerializerMethodField()
    all_sentences_life = rest_framework.serializers.SerializerMethodField()
    all_sentences_lashes = rest_framework.serializers.SerializerMethodField()
    all_sentences_sentence_years = rest_framework.serializers.SerializerMethodField()
    all_sentences_fine = rest_framework.serializers.SerializerMethodField()

    current_prison = rest_framework.serializers.SerializerMethodField()

    def get_name(self, obj):
        first = obj.forename or ''
        second = obj.surname or ''
        name = "%s %s" % (first, second)
        return name.strip()

    def get_age(self, obj):
        if obj.dob_year:
            month = obj.dob_month or 1
            day = obj.dob_day or 1
            return public.utils.calculate_age(
                date(obj.dob_year, month, day))
        return 0

    def get_files(self, obj):
        return bool(obj.files.all())

    def get_quotes(self, obj):
        return bool(obj.quotes.all())

    def get_affiliations(sef, obj):
        affiliation_objs = obj.affiliations.all()
        affiliation_names = []
        for affiliation in affiliation_objs:
            affiliation_names.append(getattr(affiliation.organisation, 'name', None))
        return affiliation_names

    def get_all_arrests_charges(self, obj):
        arrests = obj.arrests.all()
        all_charges = []
        for arrest in arrests:
            all_charges += [charge.name for charge in arrest.charged_with.all()]
        return set(all_charges)

    def get_all_arrests_activities(self, obj):
        arrests = obj.arrests.all()

        all_arrests_activities = []

        for arrest in arrests:
            if getattr(arrest.activity_persecuted_for, 'name', None):
                all_arrests_activities.append(arrest.activity_persecuted_for.name)
            if getattr(arrest.secondary_activity, 'name', None):
                all_arrests_activities.append(arrest.secondary_activity.name)
            if getattr(arrest.tertiary_activity, 'name', None):
                all_arrests_activities.append(arrest.tertiary_activity.name)

        return all_arrests_activities

    def get_all_arrests_prisons(self, obj):
        arrests = obj.arrests.all()
        prisons = []
        for arrest in arrests:
            detentions = arrest.detentions.all()
            for detention in detentions:
                if detention.prison:
                    prisons.append(detention.prison.name)
        return set(prisons)

    _all_current_prisons = None

    def get_all_current_prisons(self):
        if not self._all_current_prisons:
            current_detentions = public.utils.get_ipa_current_detentions()
            qs = (prisoners.models.PrisonerDetention.published_objects
                  .filter(id__in=current_detentions.values())
                  .select_related('arrest')
                  .select_related('prison'))

            self._all_current_prisons = {d.arrest.prisoner_id: d.prison
                                         for d in qs}
        return self._all_current_prisons

    def get_current_prison(self, prisoner):
        """
        Return the i18n'd name of a Prison, if the prisoner's current detention
        status is listed as detained, and we know the full date and prison of
        at least one detention.
        """
        prison = self.get_all_current_prisons().get(prisoner.id)
        return prison.name if prison else None

    def get_all_arrests_prison_treatments(self, obj):
        arrests = obj.arrests.all()
        treatments = []
        for arrest in arrests:
            detentions = arrest.detentions.all()
            for detention in detentions:
                detention.treatment.all()
                treatments += [treatment.name for treatment in detention.treatment.all()]
        return set(treatments)

    def get_sentence_aggregates(self, obj):
        recreate = False
        if getattr(self, 'sentence_aggregates', None) and self.sentence_aggregates['current_obj'] != obj.id:
            recreate = True

        if not getattr(self, 'sentence_aggregates', None) or recreate:
            arrests = obj.arrests.all()
            aggregated = defaultdict(list)
            aggregated['sentence_years'] = [0]

            for arrest in arrests:
                sentences = arrest.sentences.all()
                for sentence in sentences:
                    if sentence.judge:
                        first = sentence.judge.forename or ''
                        second = sentence.judge.surname or ''
                        name = "%s %s" % (first, second)
                        aggregated['judges'].append(name.strip())

                    aggregated['death_penalty'].append(sentence.death_penalty)
                    aggregated['exiled'].append(sentence.exiled)
                    aggregated['life'].append(sentence.life)

                    aggregated['fine'].append(bool(sentence.fine))
                    aggregated['number_of_lashes'].append(bool(sentence.number_of_lashes))

                    if sentence.sentence_years:
                        aggregated['sentence_years'].append(sentence.sentence_years)

            aggregated['exiled'] = any(aggregated['exiled'])
            aggregated['life'] = any(aggregated['life'])
            aggregated['death_penalty'] = any(aggregated['death_penalty'])
            aggregated['fine'] = any(aggregated['fine'])
            aggregated['number_of_lashes'] = any(aggregated['number_of_lashes'])

            self.sentence_aggregates = aggregated
            self.sentence_aggregates['current_obj'] = obj.id

        return self.sentence_aggregates

    def get_all_sentences_judges(self, obj):
        return self.get_sentence_aggregates(obj)['judges']

    def get_all_sentences_death_penalty(self, obj):
        return self.get_sentence_aggregates(obj)['death_penalty']

    def get_all_sentences_exiled(self, obj):
        return self.get_sentence_aggregates(obj)['exiled']

    def get_all_sentences_life(self, obj):
        return self.get_sentence_aggregates(obj)['life']

    def get_all_sentences_fine(self, obj):
        return self.get_sentence_aggregates(obj)['fine']

    def get_all_sentences_lashes(self, obj):
        return self.get_sentence_aggregates(obj)['number_of_lashes']

    def get_all_sentences_sentence_years(self, obj):
        return self.get_sentence_aggregates(obj)['sentence_years']

    class Meta:
        model = prisoners.models.Prisoner
        fields = core_types.serializers.PUBLISHABLE_READ_ONLY_FIELDS + (
            'id',
            'name',
            'gender',
            'age',
            'religion',
            'ethnicity',
            'latest_activity_persecuted_for_name_en',
            'latest_activity_persecuted_for_name_fa',
            'picture_200x200',
            'detention_status',
            'files',
            'quotes',
            'affiliations',
            'all_arrests_activities',
            'all_arrests_charges',
            'all_arrests_prisons',
            'all_arrests_prison_treatments',
            'all_sentences_judges',
            'all_sentences_fine',
            'all_sentences_death_penalty',
            'all_sentences_exiled',
            'all_sentences_life',
            'all_sentences_lashes',
            'all_sentences_sentence_years',
            'current_prison',
        )
