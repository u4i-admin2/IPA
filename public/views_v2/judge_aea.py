# coding: utf-8

import json
import logging

from django.contrib.staticfiles.templatetags.staticfiles import (
    static,
)
from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.db.models import (
    Case,
    Count,
    IntegerField,
    Sum,
    Value,
    When,
)
from django.utils.translation import (
    pgettext,
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
from public.utils import (
    get_view_context_with_defaults,
    SetEncoder,
)
from report.models import (
    Report,
    ReportSentence,
    ReportSentenceBehaviour
)


logger = logging.getLogger(__name__)


class JudgeAea(RestrictedQuerySetMixin, GenericAPIView):
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
        sentence_dict = ReportSentence.published_objects.filter(
            judge=self.object).aggregate(
                total_reports=Count('id'),
                total_executions=Sum(
                    Case(
                        When(
                            execution=True, then=Value(1)
                        ),
                        default=Value(0)
                    ),
                    output_field=IntegerField()),
                total_floggings=Sum(
                    Case(
                        When(
                            flogging=True, then=Value(1)
                        ),
                        default=Value(0)
                    ),
                    output_field=IntegerField()),
                total_amputationis=Sum(
                    Case(
                        When(
                            amputation=True, then=Value(1)
                        ),
                        default=Value(0)
                    ),
                    output_field=IntegerField()),
                total_victims=Sum('report__victim_count'))

        total_reports, total_executions, total_floggings, total_amputations, total_victims = map(
            sentence_dict.get, (
                'total_reports', 'total_executions', 'total_floggings', 'total_amputations', 'total_victims'))

        response_dict = {
            'judge': json_judge,
            'total_reports': total_reports,
            'total_executions': total_executions,
            'total_floggings': total_floggings,
            'total_amputations': total_amputations,
            'total_victims': total_victims
        }

        amputations_localized = pgettext(
            'Report sentence human rights violation',
            'Amputations',
        )

        executions_localized = pgettext(
            'Report sentence human rights violation',
            'Executions',
        )

        floggings_localized = pgettext(
            'Report sentence human rights violation',
            'Floggings',
        )

        humanrights_violations = {}
        all_reports = []

        humanrights_violations[amputations_localized] = list(
            ReportSentence
            .published_objects
            .filter(amputation=True)
            .values_list('id', flat=True))

        humanrights_violations[floggings_localized] = list(
            ReportSentence
            .published_objects
            .filter(flogging=True)
            .values_list('id', flat=True))

        humanrights_violations[executions_localized] = list(
            ReportSentence
            .published_objects
            .filter(execution=True)
            .values_list('id', flat=True))

        # get all the behaviours
        judge_behaviours = ReportSentenceBehaviour.published_objects.filter(
            report_sentence__judge=self.object).select_related(
            'judge_behaviour', 'report_sentence')
        behaviours = {k: [] for k in BehaviourType.published_objects.all().values_list(
            'name', flat=True)}

        for behaviour in judge_behaviours:
            # TODO: This hasn’t been properly tested due to [1]. The logic may
            # need to be revised in the future.
            #
            # [1] https://gitlab.notofilter.com/ipa/ipa/issues/98
            try:
                behaviours[behaviour.judge_behaviour.name].append(
                    behaviour.report_sentence.report.id
                )
            except (AttributeError, Report.DoesNotExist):
                pass

            all_reports.append(behaviour.report_sentence.report.id)

            # try:
            #     if (
            #         behaviour.report_sentence.amputation is True and
            #         behaviour.report_sentence.report.id not in humanrights_violations[amputations_localized]
            #     ):
            #         humanrights_violations[amputations_localized].append(
            #             behaviour.report_sentence.report.id
            #         )

            #     if (
            #         behaviour.report_sentence.execution is True and
            #         behaviour.report_sentence.report.id not in humanrights_violations[executions_localized]
            #     ):
            #         humanrights_violations[executions_localized].append(
            #             behaviour.report_sentence.report.id
            #         )

            #     if (
            #         behaviour.report_sentence.flogging is True and
            #         behaviour.report_sentence.report.id not in humanrights_violations[floggings_localized]
            #     ):
            #         humanrights_violations[floggings_localized].append(
            #             behaviour.report_sentence.report.id
            #         )
            # except (AttributeError, Report.DoesNotExist):
            #     pass
            #
            # try:
            #     report = behaviour.report_sentence.report

            #     if not chart_entity_hover_info.get(report.id, None):
            #         chart_entity_hover_info[report.id] = {
            #             'forename': report.city.name,
            #             'surname': '({victim_count} victims)'.format(
            #                 victim_count=report.victim_count or 0
            #             ),
            #         }
            # except AttributeError:
            #     pass

        chart_entity_hover_info = {}
        all_reports = \
            all_reports \
            + humanrights_violations[executions_localized] \
            + humanrights_violations[executions_localized] \
            + humanrights_violations[executions_localized]

        for id in all_reports:
            chart_entity_hover_info[id] = {
                'forename': 'Report',
                'surname': str(id),
            }

        response_dict['chart_entity_hover_info'] = chart_entity_hover_info

        # now convert set to list so we lose all the duplicate ids
        behaviours = {k: set(v) for k, v in behaviours.iteritems()}
        response_dict['behaviours'] = behaviours
        response_dict['humanrights_violations'] = humanrights_violations

        latest_report = None

        try:
            latest_report = ReportSentence.published_objects.filter(
                judge=self.object).select_related('report').order_by(
                '-report__partial_date')[0]
        except ObjectDoesNotExist:
            pass
        except IndexError:
            pass

        response_dict['report_id'] = latest_report.id if latest_report else 0
        context = {
            'title': self.object.get_name(),
            'data': json.dumps(response_dict, cls=SetEncoder),
            'head_title': _('%(name)s | %(count)d Reports') % {
                'name': self.object.get_name(),
                'count': response_dict['total_reports']
            },
            'head_description': getattr(self.object, 'biography_%s' % language)}

        try:
            context['head_image'] = self.object.picture.url
        except ValueError:
            context['head_image'] = (
                static('public/img/og_Judges_Viz_FB.png') + '?v=2019-08-28'
            )

        return Response(
            get_view_context_with_defaults(
                context,
                request,
            ),
            template_name='judge.html'
        )
