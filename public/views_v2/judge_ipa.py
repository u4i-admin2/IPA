# coding: utf-8

import json

from django.contrib.staticfiles.templatetags.staticfiles import (
    static,
)
from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.db.models import (
    Avg,
    Count,
    Sum,
)
from django.utils.translation import (
    ugettext_lazy as _,
)
from rest_framework.generics import (
    GenericAPIView,
)
from rest_framework.renderers import (
    TemplateHTMLRenderer,
)
from rest_framework.response import (
    Response,
)

from api.viewsets import (
    RestrictedQuerySetMixin,
)
from judges.models import (
    BehaviourType,
    Judge,
)
from judges.serializers import (
    JudgeSerializer,
)
from prisoners.models import (
    PrisonerArrest,
    PrisonerSentence,
    SentenceBehaviour,
)
from prisoners.renderers import (
    combine_date,
)
from public.utils import (
    get_view_context_with_defaults,
    judge_paragraph,
    SetEncoder,
)


class JudgeIpa(RestrictedQuerySetMixin, GenericAPIView):
    queryset = Judge.prefetch_queryset(Judge.published_objects.all())
    serializer_class = JudgeSerializer
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(
            self.object, context={'request': self.request})
        json_judge = serializer.data
        language = request.LANGUAGE_CODE

        # get total sentences, avg sentence, and sentence lengths
        sentence_dict = PrisonerSentence.published_objects.filter(
            judge=self.object).aggregate(
            total_years=Sum('sentence_years'),
            total_months=Sum('sentence_months'),
            total_count=Count('id'),
            average_years=Avg('sentence_years'))

        total_years, total_months, total_count, average_sentence = map(
            sentence_dict.get, (
                'total_years', 'total_months', 'total_count', 'average_years'))

        total_years = total_years or 0
        total_months = total_months or 0
        years_from_months, months = divmod(total_months, 12)
        total_time_sentenced = (total_years + years_from_months) + (months / 12)
        # if total_time_sentenced > 0 and total_count > 0:
        #     average_sentence = total_time_sentenced / total_count
        # else:
        #     average_sentence = 0

        response_dict = {
            'judge': json_judge,
            'total_sentences': total_count,
            'total_time_sentenced': round(total_time_sentenced, 1),

        }

        if average_sentence:
            response_dict['average_sentence'] = round(average_sentence, 1)
        else:
            response_dict['average_sentence'] = 0

        # get all the behaviours
        judge_behaviours = SentenceBehaviour.published_objects.filter(
            sentence__judge=self.object).select_related(
            'sentence__arrest', 'sentence__arrest__prisoner', 'behaviour_type')
        behaviours = {k: [] for k in BehaviourType.published_objects.all().values_list(
            'name', flat=True)}
        arrest_ids = set()
        for behaviour in judge_behaviours:
            try:
                behaviours[behaviour.behaviour_type.name].append(
                    behaviour.sentence.arrest.prisoner.id)
                arrest_ids.add(behaviour.sentence.arrest.id)
            except PrisonerArrest.DoesNotExist:
                pass

        # now convert set to list so we lose all the duplicate ids
        behaviours = {k: set(v) for k, v in behaviours.iteritems()}
        response_dict['behaviours'] = behaviours

        arrests = PrisonerArrest.published_objects.filter(
            sentences__judge=self.object).select_related(
            'prisoner').prefetch_related('charged_with')

        # get all the charges/activites on arrests attached to sentences from judge
        chart_entity_hover_info = {}
        for arrest in arrests:
            if not chart_entity_hover_info.get(arrest.prisoner.id, None):
                chart_entity_hover_info[arrest.prisoner.id] = {
                    'forename': arrest.prisoner.forename,
                    'surname': arrest.prisoner.surname,
                }
        response_dict['chart_entity_hover_info'] = chart_entity_hover_info

        latest_sentence_paragraph = ''
        latest_sentence_id = ''
        latest_sentence_dict = {}
        try:
            latest_sentence = PrisonerSentence.published_objects.filter(
                judge=self.object).select_related('arrest__prisoner', 'arrest').order_by(
                '-arrest__partial_date')[0]

            latest_sentence_id = latest_sentence.arrest.prisoner.id
            latest_sentence_dict['forename'] = latest_sentence.arrest.prisoner.forename
            latest_sentence_dict['surname'] = latest_sentence.arrest.prisoner.surname

            latest_sentence_dict['gender'] = latest_sentence.arrest.prisoner.gender

            if latest_sentence_dict['gender']:
                latest_sentence_dict['gender'] = latest_sentence_dict['gender'].lower()
            latest_sentence_dict['activity'] = getattr(
                latest_sentence.arrest.prisoner,
                'latest_activity_persecuted_for_name_%s' % language)
            if latest_sentence.arrest.prisoner.religion:
                latest_sentence_dict['religion'] = latest_sentence.arrest.prisoner.religion.name
            else:
                latest_sentence_dict['religion'] = None
            latest_sentence_dict['lashes'] = latest_sentence.number_of_lashes
            latest_sentence_dict['sentence_years'] = latest_sentence.sentence_years

            if language == 'en':
                latest_sentence_dict['arrest_date'] = combine_date(
                    latest_sentence.arrest.arrest_year,
                    latest_sentence.arrest.arrest_month,
                    latest_sentence.arrest.arrest_day,
                    False)
            else:
                latest_sentence_dict['arrest_date'] = combine_date(
                    latest_sentence.arrest.arrest_year_fa,
                    latest_sentence.arrest.arrest_month_fa,
                    latest_sentence.arrest.arrest_day_fa,
                    False)

            latest_sentence_paragraph = judge_paragraph(
                language, **latest_sentence_dict)

        except ObjectDoesNotExist:
            pass
        except IndexError:
            pass

        response_dict['sentence'] = latest_sentence_paragraph
        response_dict['sentence_id'] = latest_sentence_id
        try:
            response_dict['latest_sentence_prisoner_id'] = latest_sentence.arrest.prisoner.id
        except:
            response_dict['latest_sentence_prisoner_id'] = ''
        context = {
            'title': self.object.get_name(),
            'data': json.dumps(response_dict, cls=SetEncoder),
            'head_title': _('%(name)s | %(count)d Sentences Issued') % {
                'name': self.object.get_name(),
                'count': response_dict['total_sentences']
            },
            'head_description': getattr(self.object, 'biography_%s' % language)}

        try:
            context['head_image'] = self.object.picture.url
        except ValueError:
            context['head_image'] = (
                static('public/img/og_Judges_Viz_FB.png') + '?v=2019-08-28'
            )

        # If head_image isn’t a fully-qualified URL, use
        # request.build_absolute_uri to make it fully-qualified. Image URLs are
        # root-relative unless media is served directly from S3.
        if (
            isinstance(context['head_image'], basestring) and
            not context['head_image'].startswith('http')
        ):
            context['head_image'] = request.build_absolute_uri(
                self.object.picture.url
            )

        return Response(
            get_view_context_with_defaults(
                context,
                request,
            ),
            template_name='judge.html'
        )
