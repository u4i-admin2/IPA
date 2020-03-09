# coding: utf-8

from __future__ import division
from __future__ import absolute_import

import copy
from collections import (
    Counter,
    defaultdict
)
import json

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.files.storage import get_storage_class
from django.views.generic import TemplateView
from django.db.models import (
    Avg,
    Case,
    Count,
    IntegerField,
    Prefetch,
    Sum,
    Value,
    When,
    F,
    Exists,
    OuterRef
)
from django.utils.translation import (
    pgettext,
    ugettext_lazy as _
)
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from rest_framework.viewsets import ViewSet
from rest_framework.renderers import (
    TemplateHTMLRenderer,
    JSONRenderer
)
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView
)
from rest_framework.views import APIView
from easy_thumbnails.files import get_thumbnailer
from modeltranslation.utils import fallbacks

from prisons.serializers import PrisonSerializer
from prisoners.serializers import PrisonerSerializer
from public.serializers import (
    AeaSearchPageJudgeSerializer,
    AeaSearchPagePrisonSerializer,
    PrisonerStatusSummary,
    ReportStatusSummary,
    SearchPageJudgeSerializer,
    SearchPagePrisonSerializer,
    SearchPagePrisonerSerializer,
)
from prisoners.models import (
    Prisoner, Organisation, PrisonerArrest, PrisonerDetention,
    PrisonerSentence, DomesticLawViolated, InternationalLawViolated,
    ChargedWith, ActivityPersecutedFor, PrisonTreatment, DetentionStatus
)
from report.models import (
    Report,
    ReportDetention,
    HumanRightViolated,
    ReportSentence,
)
from core_types.models import (
    Religion,
    Ethnicity
)
from judges.models import (
    Judge,
    CourtAndBranch,
    JudicialPosition
)
from prisoners.renderers import combine_date
from prisons.models import (
    Prison,
    PrisonFacility
)
from api.viewsets import RestrictedQuerySetMixin
from public.utils import (
    get_ipa_current_detentions,
    get_aea_current_detentions,
    values_counter,
    get_view_context_with_defaults,
)
from public.models import Page
from public import views_v2 as public_v2_views
from public.templatetags.public_tags import (
    information_overlay,
    information_overlay_trigger_button,
)
from django.http import Http404
import logging

logger = logging.getLogger(__name__)


# prisons and prison
class Prisons(TemplateView):
    template_name = 'prisons.html'

    def make_counters(self):

        def get_names(cls):
            return cls.objects.all().values_list('name', flat=True)

        def get_counter(cls):
            return Counter({k: 0 for k in get_names(cls)})

        return {
            'religions': get_counter(Religion),
            'ethnicities': get_counter(Ethnicity),
            'activities': get_counter(ActivityPersecutedFor),
            'treatments': get_counter(PrisonTreatment),
            'charges': get_counter(ChargedWith),
            'genders': Counter({'M': 0, 'F': 0}),
            'total_prisoners': 0
        }

    def get_prison_info(self, defaults):
        # prison info keyed by prison id
        prisons = {}

        prisons_queryset = Prison \
            .published_objects \
            .annotate(
                ipa_prison=Exists(PrisonerDetention.published_objects.filter(prison__in=OuterRef('pk')))) \
            .filter(ipa_prison=True) \
            .all()

        for prison in prisons_queryset:
            dct = {
                'name': prison.name,
                'latitude': prison.latitude,
                'longitude': prison.longitude,
                'administered_by': prison.administered_by,
                'bio': prison.bio
            }
            dct.update((k, copy.copy(v)) for k, v in defaults.iteritems())
            prisons[prison.id] = dct

        return prisons

    def get_administered_by_stats(self, prisons):
        stats = Counter(prison['administered_by']
                        for prison in prisons)
        stats['ALL'] = sum(stats.values())
        return stats

    def get(self, request, *args, **kwargs):
        current_detentions = get_ipa_current_detentions()
        qs = (PrisonerDetention.published_objects
              .filter(id__in=current_detentions.values())
              .prefetch_related('arrest')
              .prefetch_related('arrest__activity_persecuted_for')
              .prefetch_related('arrest__charged_with')
              .prefetch_related('arrest__prisoner')
              .prefetch_related('arrest__prisoner__detention_status')
              .prefetch_related('arrest__prisoner__ethnicity')
              .prefetch_related('arrest__prisoner__religion')
              .prefetch_related('prison')
              .prefetch_related('treatment')
              .order_by('prison_id'))

        defaults = self.make_counters()
        prisons = self.get_prison_info(defaults)
        for detention in qs:
            prison = prisons.get(detention.prison_id, None)

            # GH 2019-07-17: This is necessary because
            # get_current_detentions() returns all detentions, including
            # some associated with prisons not queried in AeA (that is,
            # prisons not administered by pdotj or police). This could
            # more efficiently be addressed by limiting the detentions
            # returned by get_current_detentions(), but it’s a big raw SQL
            # query I’d rather not touch.
            if type(prison) != dict:
                continue

            for treatment in detention.treatment.all():
                values_counter(prison['treatments'], treatment.name)
            for charge in detention.arrest.charged_with.all():
                values_counter(prison['charges'], charge.name)
            values_counter(
                prison['religions'],
                lambda: detention.arrest.prisoner.religion.name)
            values_counter(
                prison['ethnicities'],
                lambda: detention.arrest.prisoner.ethnicity.name)
            values_counter(
                prison['genders'],
                lambda: detention.arrest.prisoner.gender)
            values_counter(
                prison['activities'],
                lambda: detention.arrest.activity_persecuted_for.name)

            prison['total_prisoners'] += 1

        cumulatives = {k: sum((p[k] for p in prisons.itervalues()), type(v)())
                       for k, v in defaults.iteritems()}

        context = self.get_context_data(**kwargs)
        context['prisons'] = json.dumps(prisons, indent=4)
        context['administered_by_stats'] = json.dumps(self.get_administered_by_stats(prisons.values()))
        context['cumulatives'] = json.dumps(cumulatives)
        context['head_image'] = (
            static('public/img/og_Prisons_Viz_FB.png') + '?v=2019-08-28'
        )
        context['head_title'] = _('%d Prisons') % len(prisons)
        context['head_description'] = _('%(prisoners_count)d political \
prisoners are currently detained in %(prisons_count)d prisons across \
Iran. Explore our visualization to find out more.') % {
            'prisoners_count': cumulatives['total_prisoners'],
            'prisons_count': len(prisons)}

        return self.render_to_response(
            get_view_context_with_defaults(
                context,
                request,
            )
        )


# prisons and prison
class AeaPrisons(TemplateView):
    template_name = 'prisons.html'

    def make_counters(self, is_aea=False):

        def get_names(cls):
            return cls.objects.all().values_list('name', flat=True)

        def get_counter(cls):
            return Counter({k: 0 for k in get_names(cls)})

        proc_violations = get_counter(DomesticLawViolated)
        proc_violations.update(get_counter(InternationalLawViolated))

        return {
            'humanrights_violations': get_counter(HumanRightViolated),
            'procedural_violations': proc_violations,
            'total_victims': 0,

        }

    def get_prison_info(self, defaults):
        # prison info keyed by prison id
        prisons = {}

        prisons_queryset = Prison \
            .published_objects \
            .annotate(
                aea_prison=Exists(ReportDetention.published_objects.filter(prison__in=OuterRef('pk')))) \
            .filter(aea_prison=True) \
            .filter(
                administered_by__in=settings.AEA_PRISON_ADMINISTERED_BY_WHITELIST) \
            .all()

        for prison in prisons_queryset:
            dct = {
                'name': prison.name,
                'latitude': prison.latitude,
                'longitude': prison.longitude,
                'administered_by': prison.administered_by,
                'bio': prison.bio
            }
            dct.update((k, copy.copy(v)) for k, v in defaults.iteritems())
            prisons[prison.id] = dct

        return prisons

    def get_administered_by_stats(self, prisons):
        stats = Counter(prison['administered_by']
                        for prison in prisons)
        stats['ALL'] = sum(stats.values())

        return stats

    def get(self, request, *args, **kwargs):
        current_detentions = get_aea_current_detentions()
        qs = (ReportDetention.published_objects
              .filter(id__in=current_detentions.values())
              .prefetch_related('prison')
              .order_by('prison_id'))

        defaults = self.make_counters(is_aea=True)
        prisons = self.get_prison_info(defaults)
        for detention in qs:
            prison = prisons.get(detention.prison_id, None)

            # GH 2019-07-17: This is necessary because
            # get_aea_current_detentions() returns all detentions, including
            # some associated with prisons not queried in AeA (that is,
            # prisons not administered by pdotj or police). This could
            # more efficiently be addressed by limiting the detentions
            # returned by get_aea_current_detentions(), but it’s a big raw SQL
            # query I’d rather not touch.
            # TODO-V2: IS THIS STILL NECESSARY
            if type(prison) != dict:
                continue

            for hrviolated in detention.report.human_right_violated.all():
                values_counter(prison['humanrights_violations'], hrviolated.name)

            for prviolated in detention.report.domestic_law_violated.all():
                values_counter(prison['procedural_violations'], prviolated.name)

            for prviolated in detention.report.international_law_violated.all():
                values_counter(prison['procedural_violations'], prviolated.name)

            prison['total_victims'] += detention.report.victim_count

        cumulatives = {k: sum((p[k] for p in prisons.itervalues()), type(v)())
                       for k, v in defaults.iteritems()}

        context = self.get_context_data(**kwargs)
        context['prisons'] = json.dumps(prisons, indent=4)
        context['administered_by_stats'] = json.dumps(self.get_administered_by_stats(prisons.values()))
        context['cumulatives'] = json.dumps(cumulatives)
        context['head_image'] = (
            static('public/img/og_Prisons_Viz_FB.png') + '?v=2019-08-28'
        )
        context['head_title'] = _('%d Prisons') % len(prisons)

        return self.render_to_response(
            get_view_context_with_defaults(
                context,
                request,
            )
        )


class PrisonView(RestrictedQuerySetMixin, GenericAPIView):
    renderer_classes = (TemplateHTMLRenderer,)
    queryset = Prison.prefetch_queryset(Prison.published_objects.all())
    serializer_class = PrisonSerializer

    def get(self, request, *args, **kwargs):
        prison = self.get_object()

        current_detentions = get_ipa_current_detentions()
        all_detentions = (PrisonerDetention.published_objects
                          .filter(prison_id=prison.id)
                          .select_related('arrest__prisoner')
                          .prefetch_related('treatment'))

        detentions = list(all_detentions.filter(id__in=current_detentions.values()))

        treatments_names = PrisonTreatment.published_objects.values_list('name', flat=True)
        mistreatments = defaultdict(list)
        for tname in treatments_names:
            mistreatments[tname] = []

        chart_entity_hover_info = {}
        for detention in all_detentions:
            for treatment in detention.treatment.all():
                mistreatments[treatment.name].append(detention.arrest.prisoner.id)
            chart_entity_hover_info[detention.arrest.prisoner.id] = {
                'forename': detention.arrest.prisoner.forename,
                'surname': detention.arrest.prisoner.surname,
                'type': detention.detention_type
            }

        serializer = self.get_serializer(prison, context={
            'request': self.request
        })

        js = {
            'prison': (JSONRenderer()
                       .render(serializer.data)),
            'political_prisoners': len(detentions),
            'mistreatments': mistreatments,
            'chart_entity_hover_info': chart_entity_hover_info
        }

        if prison.picture:
            head_image = prison.picture.url
        else:
            head_image = static('public/img/Prison.jpg') + '?v=2019-08-28'

        context = {
            'data': json.dumps(js),
            'title': prison.name,
            'head_title': _('%(prison)s | %(count)d prisoners detained') % {
                'prison': prison.name,
                'count': len(detentions),
            },
            'head_description': '%s: %s %s' % (
                prison.name,
                prison.physical_structure or '',
                prison.size_and_density or ''
            ),
            'head_image': head_image
        }

        return Response(
            get_view_context_with_defaults(
                context,
                request,
            ),
            template_name='prison.html',
        )


class AeaPrisonView(RestrictedQuerySetMixin, GenericAPIView):

    renderer_classes = (TemplateHTMLRenderer,)
    queryset = Prison.prefetch_queryset(Prison.published_objects.all())
    serializer_class = PrisonSerializer

    def get(self, request, *args, **kwargs):

        prison = self.get_object()

        if (prison.administered_by not in settings.AEA_PRISON_ADMINISTERED_BY_WHITELIST):
            return public_v2_views.Error.as_view()(
                self.request,
                status=404,
                error_title=(
                    pgettext(
                        u'Prison error message',
                        u'Prison not found',
                    )
                ),
            )

        current_detentions = get_aea_current_detentions()
        detentions = (ReportDetention.published_objects
                      .filter(id__in=current_detentions.values())
                      .prefetch_related('prison')
                      .prefetch_related('report')
                      .order_by('prison_id'))

        hr_violations = defaultdict(list)
        pr_violations = defaultdict(list)
        total_victims = 0
        chart_entity_hover_info = {}

        for detention in detentions:
            for human_right_violated in detention.report.human_right_violated.all():
                if detention.report.id not in hr_violations[human_right_violated.name]:
                    hr_violations[human_right_violated.name].append(detention.report.id)

            for domestic_law_violated in detention.report.domestic_law_violated.all():
                if detention.report.id not in pr_violations[domestic_law_violated.name]:
                    pr_violations[domestic_law_violated.name].append(detention.report.id)

            for international_law_violated in detention.report.international_law_violated.all():
                if detention.report.id not in pr_violations[international_law_violated.name]:
                    pr_violations[international_law_violated.name].append(detention.report.id)

            total_victims += detention.report.victim_count
            chart_entity_hover_info[detention.report.id] = {
                'forename': 'Report',
                'surname': str(detention.report.id)
            }

        serializer = self.get_serializer(prison, context={
            'request': self.request
        })

        js = {
            'reports': len(detentions),
            'total_victims': total_victims,
            'humanrights_violations': hr_violations,
            'procedural_violations': pr_violations,
            'chart_entity_hover_info': chart_entity_hover_info,
            'prison': (JSONRenderer()
                       .render(serializer.data)),
        }

        if prison.picture:
            head_image = prison.picture.url
        else:
            head_image = static('public/img/Prison.jpg') + '?v=2019-08-28'

        context = {
            'data': json.dumps(js),
            'title': prison.name,
            'head_title': _('%(prison)s | %(count)d prisoners detained') % {
                'prison': prison.name,
                'count': len(detentions),
            },
            'head_description': '%s: %s %s' % (
                prison.name,
                prison.physical_structure or '',
                prison.size_and_density or ''
            ),
            'head_image': head_image
        }

        return Response(
            get_view_context_with_defaults(
                context,
                request,
            ),
            template_name='prison.html',
        )


# prisoners and prisoner
class Prisoners(TemplateView):
    template_name = 'prisoners.html'

    # this should parse into farsi translation
    years = unicode(PrisonerSentence._meta.get_field('sentence_years').verbose_name)
    fine = unicode(PrisonerSentence._meta.get_field('fine').verbose_name)
    lashes = unicode(PrisonerSentence._meta.get_field('number_of_lashes').verbose_name)
    execution = unicode(PrisonerSentence._meta.get_field('death_penalty').verbose_name)
    exiled = unicode(PrisonerSentence._meta.get_field('exiled').verbose_name)
    sentence_types = [years, fine, lashes, execution, exiled]

    def parse_detention_status(self, status, detained, year):
        if status:
            if detained:
                return 'DETAINED'
            elif status == 3:
                return 'EXECUTED'
            elif status == 7:
                return 'PASSED_AWAY'
            elif not detained:
                return 'RELEASED'
        return 'UNKNOWN'

    def get(self, request, *args, **kwargs):
        language = request.LANGUAGE_CODE
        context = self.get_context_data(**kwargs)

        prisoner_lookup = {}
        religions = {k: [] for k in Religion.published_objects.all().values_list('name', flat=True)}
        ethnicities = {k: [] for k in Ethnicity.published_objects.all().values_list('name', flat=True)}
        activities = {k: [] for k in ActivityPersecutedFor.published_objects.all().values_list('name', flat=True)}
        charges = {k: [] for k in ChargedWith.published_objects.all().values_list('name', flat=True)}
        treatments = {k: [] for k in PrisonTreatment.published_objects.all().values_list('name', flat=True)}
        sentences = {unicode(_(k)): [] for k in self.sentence_types}

        # basic prisoner info
        religions.update({unicode(_('Unknown')): []})
        ethnicities.update({unicode(_('Unknown')): []})
        prisoners = (Prisoner.published_objects.all()
                     .select_related('religion')
                     .select_related('ethnicity')
                     .select_related('detention_status'))

        for pris in prisoners:

            if pris.religion:
                religion = pris.religion.name
            else:
                religion = unicode(_('Unknown'))

            if pris.ethnicity:
                ethnicity = pris.ethnicity.name
            else:
                ethnicity = unicode(_('Unknown'))

            picture = ""
            if pris.picture:
                thumbnailer = get_thumbnailer(pris.picture)
                try:
                    picture = thumbnailer.get_thumbnail(
                        {'upscale': True, 'size': (30, 30), 'crop': 'smart'}).url
                except Exception:
                    pass

            for activity_prefix in (
                'latest_activity_persecuted_for_name_',
                'latest_secondary_activity_name_',
                'latest_tertiary_activity_name_',
            ):
                activity = getattr(pris, activity_prefix + language)

                if activity:
                    try:
                        activities[activity].append(pris.id)
                    except KeyError:
                        pass

            latest_activity = getattr(
                pris,
                'latest_activity_persecuted_for_name_' + language,
                None
            )

            religions[religion].append(pris.id)
            ethnicities[ethnicity].append(pris.id)

            prisoner_lookup[pris.id] = {
                'forename': pris.forename,
                'surname': pris.surname,
                'picture': picture,
                'ethnicity': ethnicity,
                'religion': religion,
                'dob_en': combine_date(pris.dob_year, pris.dob_month, pris.dob_day),
                'dob_fa': combine_date(pris.dob_year_fa, pris.dob_month_fa, pris.dob_day_fa),
                'latest_activity': latest_activity,
                'detention_status': self.parse_detention_status(
                    getattr(pris.detention_status, 'pk', None),
                    getattr(pris.detention_status, 'detained', None),
                    pris.detention_year
                ),
            }

        detention_stats = Counter(prisoner.get('detention_status') for prisoner in prisoner_lookup.values())
        detention_stats['ALL'] = sum(detention_stats.values())

        # get latest arrest for all prisoners so we can get charges
        latest_arrests = PrisonerArrest.published_objects.all().prefetch_related(
            'charged_with').select_related('prisoner').distinct('prisoner__id').order_by(
            'prisoner__id', 'arrest_year', 'arrest_month', 'arrest_day')

        latest_arrest_ids = []
        for arrest in latest_arrests:
            # we do this check to filter out unpublished prisoners
            if prisoner_lookup.get(arrest.prisoner.id, None):
                latest_arrest_ids.append(arrest.id)
                prisoner_charges = []
                for charge in arrest.charged_with.all():
                    charges[charge.name].append(arrest.prisoner.id)
                    prisoner_charges.append(charge.name)
                    prisoner_lookup[arrest.prisoner.id]['charges'] = prisoner_charges

        # use arrest ids to get latest sentences and link back to get prisoner ids
        latest_sentences = PrisonerSentence.published_objects.filter(
            arrest__id__in=latest_arrest_ids).select_related('arrest__prisoner').distinct(
            'arrest__id').order_by('arrest__id', '-sentence_type__finality', '-id')
        total_years = 0
        for sentence in latest_sentences:
            # note, not all prisoners will have a sentence at time of writing
            # we do this check to filter out unpublished prisoners
            if prisoner_lookup.get(sentence.arrest.prisoner.id, None):
                if sentence.sentence_years:
                    sentences[unicode(_(self.years))].append(
                        sentence.arrest.prisoner.id)
                    if prisoner_lookup[sentence.arrest.prisoner.id]['detention_status'] == 'DETAINED':
                        total_years += sentence.sentence_years
                if sentence.fine:
                    sentences[unicode(_(self.fine))].append(
                        sentence.arrest.prisoner.id)
                if sentence.number_of_lashes:
                    sentences[unicode(_(self.lashes))].append(
                        sentence.arrest.prisoner.id)
                if sentence.exiled:
                    sentences[unicode(_(self.exiled))].append(
                        sentence.arrest.prisoner.id)
                if sentence.death_penalty:
                    sentences[unicode(_(self.execution))].append(
                        sentence.arrest.prisoner.id)

                prisoner_lookup[sentence.arrest.prisoner.id]['sentence'] = {
                    unicode(_(self.fine)): sentence.fine,
                    unicode(_(self.execution)): sentence.death_penalty,
                    unicode(_(self.lashes)): sentence.number_of_lashes,
                    unicode(_(self.exiled)): sentence.exiled,
                    unicode(_(self.years)): sentence.sentence_years,
                }

        # get latest detention for all prisoners
        # in order to get treatment in prison
        detentions = PrisonerDetention.published_objects.filter(
            arrest__id__in=latest_arrest_ids).prefetch_related(
            'treatment').select_related(
            'arrest__prisoner').distinct('arrest__id').order_by(
            'arrest__id', 'detention_year', 'detention_month', 'detention_day')

        for detention in detentions:
            prisoner_treatments = []
            for treatment in detention.treatment.all():
                if prisoner_lookup.get(detention.arrest.prisoner.id, None):
                    treatments[treatment.name].append(
                        detention.arrest.prisoner.id)
                    prisoner_treatments.append(treatment.name)
                    prisoner_lookup[detention.arrest.prisoner.id]['treatments'] = prisoner_treatments

        dimensions = {}
        dimensions['religion'] = religions
        dimensions['ethnicity'] = ethnicities
        dimensions['activity'] = activities
        dimensions['sentences'] = sentences
        dimensions['charges'] = charges
        dimensions['mistreatments'] = treatments

        request_context = RequestContext(request)

        django_prerendered_information_overlay = {
            'prisoners': (
                information_overlay(
                    request_context,
                    slug='prisoners',
                    text=pgettext(
                        'Prisoner(s) information box description',
                        'Prisoners description',
                    ),
                    title=pgettext(
                        'Prisoner(s) information box title',
                        'Prisoners',
                    ),
                )
            ),
        }

        django_prerendered_information_overlay_trigger_button = {
            'prisoners': (
                information_overlay_trigger_button(
                    request_context,
                    position_type='absolute',
                    information_overlay_slug='prisoners',
                )
            ),
        }

        django_prerendered_component_html = {
            'information_overlay': django_prerendered_information_overlay,
            'information_overlay_trigger_button': django_prerendered_information_overlay_trigger_button,
        }

        context['dimensions'] = json.dumps(dimensions)
        context['prisoner_lookup'] = json.dumps(prisoner_lookup)
        context['detention_stats'] = json.dumps(detention_stats)
        context['head_title'] = _(
            '%d Political Prisoners') % detention_stats['ALL']
        context['head_description'] = _("%(count)d political prisoners \
are currently serving a cumulative total of %(total_years)d years in \
Iran's prisons. Explore our visualization to find out more.") % {
            'count': detention_stats['DETAINED'],
            'total_years': total_years}
        context['head_image'] = (
            static('public/img/og_Prisons_Viz_FB.png') + '?v=2019-08-28'
        )
        context['django_prerendered_component_html'] = django_prerendered_component_html

        return self.render_to_response(
            get_view_context_with_defaults(
                context,
                request,
            ),
        )


class PrisonerView(RestrictedQuerySetMixin, GenericAPIView):
    queryset = Prisoner.prefetch_queryset(Prisoner.published_objects.all())
    serializer_class = PrisonerSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    exclude = ('comments', 'created', 'created_by',
               'ethnicity_id', 'home_countries_ids',
               'religion_id', 'sources', 'updated', 'updated_by')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, fields=self.exclude, context={'request': self.request})
        json_prisoner = JSONRenderer().render(serializer.data)
        biography = ''
        sentence = ''

        if isinstance(serializer.data['picture'], basestring):
            head_image = serializer.data['picture']
        else:
            head_image = (
                static('public/img/og_Prisoners_Viz_FB.png') + '?v=2019-08-28'
            )

        latest_arest = PrisonerArrest.published_objects.filter(
            prisoner=self.object).last()
        latest_sentence = PrisonerSentence.published_objects.filter(
            arrest=latest_arest).first()
        if latest_sentence:
            if latest_sentence.death_penalty:
                sentence = _("Execution")
            elif latest_sentence.exiled:
                sentence = _("Exile")
            elif latest_sentence.life:
                sentence = _("Life")
            elif latest_sentence.social_depravation:
                sentence = latest_sentence.social_depravation
            elif latest_sentence.fine:
                sentence = _("Fine: %s Rial") % latest_sentence.fine
            elif latest_sentence.number_of_lashes:
                sentence = _("%s lashes") % latest_sentence.number_of_lashes
            elif latest_sentence.sentence_years:
                if latest_sentence.sentence_years > 1:
                    sentence = _("%s years") % latest_sentence.sentence_years
                else:
                    sentence = _("%s year") % latest_sentence.sentence_years
            elif latest_sentence.sentence_months:
                if latest_sentence.sentence_months > 1:
                    sentence = _("%s months") % latest_sentence.sentence_months
                else:
                    sentence = _("%s month") % latest_sentence.sentence_months

        if self.object.biography:
            biography = ' | %s' % self.object.biography

        request_context = RequestContext(request)

        information_overlay_trigger_button_activity_persecuted_for = {}
        information_overlays_activity_persecuted_for = []

        for activity_persecuted_for in ActivityPersecutedFor.published_objects.all():
            information_overlay_slug = (
                'activity_persecuted_for_{id}'.format(
                    id=activity_persecuted_for.id
                )
            )

            information_overlay_trigger_button_activity_persecuted_for[activity_persecuted_for.id] = (
                information_overlay_trigger_button(
                    request_context,
                    position_type='absolute',
                    information_overlay_slug=information_overlay_slug,
                )
            )

            information_overlays_activity_persecuted_for.append(
                information_overlay(
                    request_context,
                    slug=information_overlay_slug,
                    text=getattr(
                        activity_persecuted_for,
                        'name_{language_code}'.format(
                            language_code=request.LANGUAGE_CODE,
                        ),
                    ),
                    title=getattr(
                        activity_persecuted_for,
                        'name_{language_code}'.format(
                            language_code=request.LANGUAGE_CODE,
                        ),
                    ),
                )
            )

        information_overlay_trigger_button_charged_with = {}
        information_overlays_charged_with = []

        for charged_with in ChargedWith.published_objects.all():
            information_overlay_slug = (
                'charged_with_by_{id}'.format(
                    id=charged_with.id
                )
            )

            information_overlay_trigger_button_charged_with[charged_with.id] = (
                information_overlay_trigger_button(
                    request_context,
                    position_type='absolute',
                    information_overlay_slug=information_overlay_slug,
                )
            )

            information_overlays_charged_with.append(
                information_overlay(
                    request_context,
                    slug=information_overlay_slug,
                    text=getattr(
                        charged_with,
                        'name_{language_code}'.format(
                            language_code=request.LANGUAGE_CODE,
                        ),
                    ),
                    title=getattr(
                        charged_with,
                        'name_{language_code}'.format(
                            language_code=request.LANGUAGE_CODE,
                        ),
                    ),
                )
            )

        django_prerendered_information_overlay = {
            'activity_persecuted_for': information_overlays_activity_persecuted_for,
            'arrests': (
                information_overlay(
                    request_context,
                    slug='arrests',
                    text=pgettext(
                        'Prisoner(s) information box description',
                        'Arrests description',
                    ),
                    title=pgettext(
                        'Prisoner(s) information box title',
                        'Arrests',
                    ),
                )
            ),
            'charged_with': information_overlays_charged_with,
            'sentence': (
                information_overlay(
                    request_context,
                    slug='sentence',
                    text=pgettext(
                        'Prisoner(s) information box description',
                        'Sentence description',
                    ),
                    title=pgettext(
                        'Prisoner(s) information box title',
                        'Sentence',
                    ),
                )
            ),
        }

        django_prerendered_information_overlay_trigger_button = {
            'arrests': (
                information_overlay_trigger_button(
                    request_context,
                    position_type='absolute',
                    information_overlay_slug='arrests',
                )
            ),
            'sentence': (
                information_overlay_trigger_button(
                    request_context,
                    position_type='absolute',
                    information_overlay_slug='sentence',
                )
            ),
        }

        django_prerendered_component_html = {
            'information_overlay': django_prerendered_information_overlay,
            'information_overlay_trigger_button': django_prerendered_information_overlay_trigger_button,
        }

        js_prerendered_component_html_encoded = json.dumps({
            'informationOverlayTriggerButton': {
                'activityPersecutedForById': (
                    information_overlay_trigger_button_activity_persecuted_for
                ),
                'chargedWithById': (
                    information_overlay_trigger_button_charged_with
                ),
            }
        })

        context = {
            'prisoner': json_prisoner,
            'title': self.object.get_name(),
            'head_title': '%s - %s' % (
                self.object.get_name(), getattr(self.object, 'latest_activity_persecuted_for_name_%s' % request.LANGUAGE_CODE)),
            'head_description': '%s | %s%s' % (self.object.get_name(), sentence, biography),
            'head_image': head_image,
            'django_prerendered_component_html': django_prerendered_component_html,
            'js_prerendered_component_html_encoded': js_prerendered_component_html_encoded,
        }

        return Response(
            get_view_context_with_defaults(
                context,
                request,
            ),
            template_name='prisoner.html'
        )


class Judges(TemplateView):
    template_name = 'judges.html'
    media_storage = get_storage_class()()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        judges_dict = {}
        with fallbacks(False):
            judges_qs = Judge \
                .published_objects \
                .filter(is_judge=True) \
                .annotate(
                    ipa_judge=Exists(PrisonerSentence.published_objects.filter(judge__in=OuterRef('pk')))) \
                .filter(ipa_judge=True) \
                .all() \
                .values('id',
                        'forename',
                        'surname',
                        'picture',
                        'biography')

        # judge info keyed by judge id
        for judge in judges_qs.iterator():
            judges_dict[judge.pop('id')] = judge

        judge_stats = (
            PrisonerSentence.published_objects
            .filter(
                judge_id__in=judges_dict.keys()
            )
            .values('judge_id')
            .annotate(
                total_mistreatments=F('judge__mistreatments_count'),
                total_verdicts=Count('id'),
                total_years=Sum('sentence_years'),
                average_years=Avg('sentence_years'),
                total_months=Sum('sentence_months'),
                average_months=Avg('sentence_months'),
                total_lashes=Sum('number_of_lashes'),
                total_executions=Sum(
                    Case(
                        When(
                            death_penalty=True, then=Value(1)
                        ),
                        default=Value(0)
                    ),
                    output_field=IntegerField()
                ),
            )
            .order_by('judge_id')
        )

        empty_stats = {'total_months': 0,
                       'total_lashes': 0,
                       'prisoners_sentenced': 0,
                       'average_months': 0,
                       'total_mistreatments': 0,
                       'average_years': 0,
                       'total_years': 0,
                       'total_executions': 0,
                       'total_verdicts': 0}

        # add judge stats to each judge
        for stats in judge_stats:
            for key, value in stats.iteritems():
                if not value:
                    stats[key] = 0
                elif isinstance(value, float):
                    stats[key] = round(value, 1)

            judges_dict[stats.pop('judge_id')]['stats'] = stats

        for judge in judges_dict:
            # Set `picture_url` (fully-qualified picture URL; `picture` is just the path)
            if len(judges_dict[judge].get('picture', '')) > 0:
                judges_dict[judge]['picture_url'] = self.media_storage.url(
                    judges_dict[judge]['picture']
                )
            else:
                judges_dict[judge]['picture_url'] = None

            # Add `stats` to empty_stats if not set
            if 'stats' not in judges_dict[judge]:
                judges_dict[judge]['stats'] = empty_stats

        # get total individual prisoners sentenced by each judge (ie total verdicts with duplicates removed)
        prisoners_by_judge = PrisonerSentence.published_objects.filter(judge_id__in=judges_dict.keys()).values('judge_id').annotate(
            prisoners_sentenced=Count('arrest__prisoner', distinct=True)).order_by('judge_id')

        for detail in prisoners_by_judge.iterator():
            judges_dict[detail.pop('judge_id')]['stats'].update(detail)

        judge_count = judges_qs.count()

        request_context = RequestContext(request)

        django_prerendered_information_overlay = {
            'judges': (
                information_overlay(
                    request_context,
                    slug='judges',
                    text=pgettext(
                        'Judges information box description',
                        'Judges description',
                    ),
                    title=pgettext(
                        'Judges information box title',
                        'Judges',
                    ),
                )
            ),
            'lashes': (
                information_overlay(
                    request_context,
                    slug='lashes',
                    text=pgettext(
                        'Judges information box description',
                        'Lashes description',
                    ),
                    title=pgettext(
                        'Judges information box title',
                        'Lashes',
                    ),
                )
            ),
            'misconduct': (
                information_overlay(
                    request_context,
                    slug='misconduct',
                    text=pgettext(
                        'Judges information box description',
                        'Misconduct description',
                    ),
                    title=pgettext(
                        'Judges information box title',
                        'Misconduct',
                    ),
                )
            ),
        }

        django_prerendered_information_overlay_trigger_button = {
            'judges': (
                information_overlay_trigger_button(
                    request_context,
                    position_type='absolute',
                    information_overlay_slug='judges',
                )
            ),
        }

        context['django_prerendered_component_html'] = {
            'information_overlay': (
                django_prerendered_information_overlay
            ),
            'information_overlay_trigger_button': (
                django_prerendered_information_overlay_trigger_button
            ),
        }

        js_prerendered_information_overlay_trigger_button = {
            'lashes': (
                information_overlay_trigger_button(
                    request_context,
                    position_type='absolute',
                    information_overlay_slug='lashes',
                )
            ),
            'misconduct': (
                information_overlay_trigger_button(
                    request_context,
                    position_type='absolute',
                    information_overlay_slug='misconduct',
                )
            ),
        }

        context['js_prerendered_component_html_encoded'] = json.dumps({
            'informationOverlayTriggerButton': (
                js_prerendered_information_overlay_trigger_button
            ),
        })

        context['judges'] = json.dumps(judges_dict)
        context['head_image'] = (
            static('public/img/og_Judges_Viz_FB.png') + '?v=2019-08-28'
        )
        context['head_title'] = _('%d Judges') % judge_count
        context['head_description'] = _("%(judges_count)d judges have handed \
out %(sentences_count)d sentences to Iran's political prisoners. Explore \
our visualization to find out more.") % {
            'judges_count': judge_count,
            'sentences_count': PrisonerSentence.published_objects.count()}

        return self.render_to_response(
            get_view_context_with_defaults(
                context,
                request,
            ),
        )


class AeaJudges(TemplateView):
    template_name = 'judges.html'
    media_storage = get_storage_class()()

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)

        judges_dict = {}
        with fallbacks(False):
            judges_qs = Judge \
                .published_objects \
                .filter(is_judge=True) \
                .annotate(
                    aea_judge=Exists(ReportSentence.published_objects.filter(judge__in=OuterRef('pk')))) \
                .filter(aea_judge=True) \
                .all() \
                .values('id',
                        'forename',
                        'surname',
                        'picture',
                        'biography')

        # judge info keyed by judge id
        for judge in judges_qs.iterator():
            judges_dict[judge.pop('id')] = judge

            judge_stats = (
                ReportSentence.published_objects
                .filter(
                    judge_id__in=judges_dict.keys()
                )
                .values('judge_id')
                .annotate(
                    total_reports=Count('id'),
                    total_mistreatments=F('judge__aea_mistreatments_count'),
                    total_executions=Sum(
                        Case(
                            When(
                                execution=True, then=Value(1)
                            ),
                            default=Value(0)
                        ),
                        output_field=IntegerField()),
                    total_flogging=Sum(
                        Case(
                            When(
                                flogging=True, then=Value(1)
                            ),
                            default=Value(0)
                        ),
                        output_field=IntegerField()),
                    total_amputation=Sum(
                        Case(
                            When(
                                amputation=True, then=Value(1)
                            ),
                            default=Value(0)
                        ),
                        output_field=IntegerField()),
                    total_victims=Sum('report__victim_count')
                )
                .order_by('judge_id')
            )

            # add judge stats to each judge
            for stats in judge_stats:
                for key, value in stats.iteritems():
                    if not value:
                        stats[key] = 0
                    elif isinstance(value, float):
                        stats[key] = round(value, 1)

                judges_dict[stats.pop('judge_id')]['stats'] = stats

        empty_stats = {
            'total_reports': 0,
            'total_executions': 0,
            'total_flogging': 0,
            'total_amputation': 0,
            'total_victims': 0,
        }

        for judge in judges_dict:
            # Set `picture_url` (fully-qualified picture URL; `picture` is just the path)
            if len(judges_dict[judge].get('picture', '')) > 0:
                judges_dict[judge]['picture_url'] = self.media_storage.url(
                    judges_dict[judge]['picture']
                )
            else:
                judges_dict[judge]['picture_url'] = None

            # Add `stats` to empty_stats if not set
            if 'stats' not in judges_dict[judge]:
                judges_dict[judge]['stats'] = empty_stats

        # get total individual prisoners sentenced by each judge (ie total verdicts with duplicates removed)
        prisoners_by_judge = PrisonerSentence.published_objects.filter(judge_id__in=judges_dict.keys()).values('judge_id').annotate(
            prisoners_sentenced=Count('arrest__prisoner', distinct=True)).order_by('judge_id')

        for detail in prisoners_by_judge.iterator():
            judges_dict[detail.pop('judge_id')]['stats'].update(detail)

        judge_count = judges_qs.count()

        context['judges'] = json.dumps(judges_dict)
        context['head_image'] = (
            static('public/img/og_Judges_Viz_FB.png') + '?v=2019-08-28'
        )
        context['head_title'] = _('%d Judges') % judge_count
        context['head_description'] = _("%(judges_count)d judges have handed \
out %(sentences_count)d sentences to Iran's political prisoners. Explore \
our visualization to find out more.") % {
            'judges_count': judge_count,
            'sentences_count': PrisonerSentence.published_objects.count()}

        return self.render_to_response(
            get_view_context_with_defaults(
                context,
                request,
            ),
        )


class Search(TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        dimensions = {}
        # prisoners
        dimensions['religions'] = [k for k in Religion.published_objects.all().values_list('name', flat=True)]
        dimensions['ethnicities'] = [k for k in Ethnicity.published_objects.all().values_list('name', flat=True)]
        dimensions['activities'] = [k for k in ActivityPersecutedFor.published_objects.all().values_list('name', flat=True)]
        dimensions['charges'] = [k for k in ChargedWith.published_objects.all().values_list('name', flat=True)]
        dimensions['treatments'] = [k for k in PrisonTreatment.published_objects.all().values_list('name', flat=True)]
        dimensions['prisons'] = [k for k in Prison
                                 .published_objects
                                 .annotate(
                                     ipa_prison=Exists(PrisonerDetention.published_objects.filter(prison__in=OuterRef('pk'))))
                                 .filter(ipa_prison=True)
                                 .all()
                                 .values_list('name', flat=True)]
        dimensions['statuses'] = [k for k in DetentionStatus.published_objects.all().values_list('name', flat=True)]

        dimensions['judges'] = [j.get_name() for j in Judge
                                .published_objects
                                .annotate(
                                    ipa_judge=Exists(PrisonerSentence.published_objects.filter(judge__in=OuterRef('pk'))))
                                .filter(ipa_judge=True)
                                .all()]

        dimensions['affiliations'] = [affiliation_name for affiliation_name in
                                      Organisation.published_objects.all().values_list('name', flat=True)]

        dimensions['court_and_branch'] = [k for k in CourtAndBranch.published_objects.all().values_list('name', flat=True)]
        dimensions['judicial_position'] = [k for k in JudicialPosition.published_objects.all().values_list('name', flat=True)]
        dimensions['judge_type'] = [unicode(k[1]) for k in Judge.JUDGE_TYPE]

        # prisons
        dimensions['prison_administrators'] = [unicode(k[1]) for k in Prison.ADMINISTERED_BY_CHOICES]
        dimensions['prison_facilities'] = [k for k in PrisonFacility.published_objects.all().values_list('name', flat=True)]

        context['dimensions'] = json.dumps(dimensions)

        context['head_description'] = None
        context['head_title'] = pgettext(
            'Search',
            # Transators: Search/social media title for search page
            'Search',
        )

        context['head_image'] = None

        return self.render_to_response(
            get_view_context_with_defaults(
                context,
                request,
            ),
        )


class AeaSearch(TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        dimensions = {}
        # prisoners
        dimensions['religions'] = [k for k in Religion.published_objects.all().values_list('name', flat=True)]
        dimensions['ethnicities'] = [k for k in Ethnicity.published_objects.all().values_list('name', flat=True)]
        dimensions['activities'] = [k for k in ActivityPersecutedFor.published_objects.all().values_list('name', flat=True)]
        dimensions['charges'] = [k for k in ChargedWith.published_objects.all().values_list('name', flat=True)]
        dimensions['treatments'] = [k for k in PrisonTreatment.published_objects.all().values_list('name', flat=True)]
        dimensions['prisons'] = [k for k in Prison
                                 .published_objects
                                 .annotate(
                                     aea_prison=Exists(ReportDetention.published_objects.filter(prison__in=OuterRef('pk'))))
                                 .filter(aea_prison=True)
                                 .filter(
                                     administered_by__in=settings.AEA_PRISON_ADMINISTERED_BY_WHITELIST)
                                 .all()
                                 .values_list('name', flat=True)]
        dimensions['statuses'] = [k for k in DetentionStatus.published_objects.all().values_list('name', flat=True)]

        dimensions['judges'] = [j.get_name() for j in Judge
                                .published_objects
                                .annotate(
                                    aea_judge=Exists(ReportSentence.published_objects.filter(judge__in=OuterRef('pk'))))
                                .filter(aea_judge=True)
                                .all()]

        dimensions['affiliations'] = [affiliation_name for affiliation_name in
                                      Organisation.published_objects.all().values_list('name', flat=True)]

        dimensions['court_and_branch'] = [k for k in CourtAndBranch.published_objects.all().values_list('name', flat=True)]
        dimensions['judicial_position'] = [k for k in JudicialPosition.published_objects.all().values_list('name', flat=True)]
        dimensions['judge_type'] = [unicode(k[1]) for k in Judge.JUDGE_TYPE]

        # prisons
        dimensions['prison_administrators'] = [unicode(k[1]) for k in settings.AEA_PRISON_ADMINISTERED_BY_WHITELIST]
        dimensions['prison_facilities'] = [k for k in PrisonFacility.published_objects.all().values_list('name', flat=True)]

        context['dimensions'] = json.dumps(dimensions)

        context['head_description'] = None
        context['head_title'] = pgettext(
            'Search',
            # Transators: Search/social media title for search page
            'Search',
        )

        context['head_image'] = None

        return self.render_to_response(
            get_view_context_with_defaults(
                context,
                request,
            ),
        )


"""
ENDPOINTS
"""


class PrisonerSummaryView(RestrictedQuerySetMixin, RetrieveAPIView):
    """ Endpoint used on judge and prison page to get a lightweight prisoner """

    queryset = Prisoner.published_objects.all()
    serializer_class = PrisonerStatusSummary


class ReportSummaryView(RestrictedQuerySetMixin, RetrieveAPIView):
    """ Endpoint used on judge and prison page to get a lightweight report """

    queryset = Report.published_objects.all()
    serializer_class = ReportStatusSummary


class SentencesByJudgeView(APIView):
    """ Endpoint used on judges page to return info about sentences and prisoners """

    media_storage = get_storage_class()()

    def get(self, request, *args, **kwargs):
        language = request.LANGUAGE_CODE

        judge_id = self.kwargs['judge_id']
        sentences = PrisonerSentence.published_objects.filter(judge_id=judge_id).values(
            'death_penalty', 'fine', 'number_of_lashes',
            'sentence_type__finality', 'exiled', 'life',
            'sentence_months', 'sentence_years', 'arrest__prisoner_id')

        prisoner_ids = [sentence['arrest__prisoner_id'] for sentence in sentences]

        all_fields = ['id', 'forename', 'surname', 'picture', 'detention_status__detained']
        fa_fields = ['latest_activity_persecuted_for_name_fa', 'dob_year_fa', 'dob_month_fa', 'dob_day_fa',
                     'detention_status__name_fa']
        en_fields = ['latest_activity_persecuted_for_name_en', 'dob_year', 'dob_month', 'dob_day',
                     'detention_status__name_en']

        if language == 'en':
            all_fields += en_fields
        else:
            all_fields += fa_fields

        prisoners = list(
            Prisoner
            .published_objects
            .filter(id__in=prisoner_ids)
            .values(*set(all_fields))
        )

        for prisoner in prisoners:
            if len(prisoner.get('picture', '')) > 0:
                prisoner['picture_url'] = self.media_storage.url(
                    prisoner['picture']
                )
            else:
                prisoner['picture_url'] = None

        return Response({'sentences': sentences, 'prisoners': prisoners})


class SearchPrisoners(RestrictedQuerySetMixin, ViewSet):
    """ Endpoint used on search page to provide super querylite prisoner """
    serializer_class = SearchPagePrisonerSerializer

    def list(self, request):
        # res = cache.get('search', None)
        # if res:
        #     print "from cache"
        #     return Response(res)
        # else:
        #     print "not from cache"

        queryset = Prisoner.published_objects.all().prefetch_related(
            'religion',
            'ethnicity',
            Prefetch('arrests', queryset=PrisonerArrest.published_objects.all().order_by(
                '-arrest_year', '-arrest_month', '-arrest_day')),
            'files',
            'quotes',
            'affiliations',
            'detention_status',
            Prefetch(
                'arrests__detentions',
                queryset=PrisonerDetention.published_objects.all().order_by(
                    '-detention_year', '-detention_month', '-detention_day')),
            'arrests__activity_persecuted_for',
            'arrests__charged_with',
            'arrests__sentences__judge',
            'arrests__detentions',
            'arrests__detentions__prison',
            'arrests__detentions__treatment').select_related(
            'detention_status'
        )

        serializer = self.serializer_class(
            queryset, many=True, context={'request': request})

        # cache.set('search', serializer.data, 1000)
        return Response(serializer.data)


class AeaSearchPrisons(RestrictedQuerySetMixin, ViewSet):
    """ Endpoint used on search page to provide minimal prison """
    serializer_class = AeaSearchPagePrisonSerializer

    def list(self, request):

        queryset = Prison \
            .published_objects \
            .annotate(
                aea_prison=Exists(ReportDetention.published_objects.filter(prison__in=OuterRef('pk')))) \
            .filter(aea_prison=True) \
            .filter(
                administered_by__in=settings.AEA_PRISON_ADMINISTERED_BY_WHITELIST) \
            .all() \
            .prefetch_related(
                'files',
                'quotes',
                'facilities',
                'detentions',
                'detentions__treatment',
                'detentions__arrest__activity_persecuted_for',)

        serializer = self.serializer_class(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class SearchPrisons(RestrictedQuerySetMixin, ViewSet):
    """ Endpoint used on search page to provide minimal prison """
    serializer_class = SearchPagePrisonSerializer

    def list(self, request):

        queryset = Prison \
            .published_objects \
            .annotate(
                ipa_prison=Exists(PrisonerDetention.published_objects.filter(prison__in=OuterRef('pk')))) \
            .filter(ipa_prison=True) \
            .all() \
            .prefetch_related(
                'files',
                'quotes',
                'facilities',
                'detentions',
                'detentions__treatment',
                'detentions__arrest__activity_persecuted_for',)

        serializer = self.serializer_class(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class AeaSearchJudges(RestrictedQuerySetMixin, ViewSet):
    """ Endpoint used on search page to provide minimal judge """
    serializer_class = AeaSearchPageJudgeSerializer

    def list(self, request):

        queryset = Judge \
            .published_objects \
            .annotate(
                aea_judge=Exists(ReportSentence.published_objects.filter(judge__in=OuterRef('pk')))) \
            .filter(aea_judge=True) \
            .all() \
            .prefetch_related(
                'files',
                'quotes',
                'judicial_position',
                'court_and_branch',
                'positions',)

        serializer = self.serializer_class(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class SearchJudges(RestrictedQuerySetMixin, ViewSet):
    """ Endpoint used on search page to provide minimal judge """
    serializer_class = SearchPageJudgeSerializer

    def list(self, request):

        queryset = Judge \
            .published_objects \
            .annotate(
                ipa_judge=Exists(PrisonerSentence.published_objects.filter(judge__in=OuterRef('pk')))) \
            .filter(ipa_judge=True) \
            .all() \
            .prefetch_related(
                'files',
                'quotes',
                'judicial_position',
                'court_and_branch',
                'positions',)

        serializer = self.serializer_class(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class Robots(TemplateView):
    template_name = 'robots.txt'


class PageDetail(TemplateView):
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context = super(PageDetail, self).get_context_data(**kwargs)

        slug = self.kwargs.pop('slug', None)
        if slug:
            try:
                page = Page.objects.get(
                    is_published=True,
                    site=self.request.ipa_site,
                    slug=slug,
                )
                context['page'] = page
            except ObjectDoesNotExist:
                raise Http404
        else:
            try:
                page = Page.objects.get(
                    is_published=True,
                    site=self.request.ipa_site,
                    slug='about',
                )
                context['page'] = page
            except ObjectDoesNotExist:
                raise Http404

        context['pages'] = (
            Page.objects
            .filter(
                is_published=True,
                site=self.request.ipa_site,
            )
            .only('slug', 'title')
        )

        context['head_description'] = None
        context['head_title'] = page.title
        context['head_image'] = None

        return get_view_context_with_defaults(
            context,
            self.request,
        )
