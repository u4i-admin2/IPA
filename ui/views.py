import django.views.generic
import django.views.generic.base

import api.viewsets
import judges.models
import prisons.models
import prisoners.models
import report.models
import ui.decorators


class VarsMixin(django.views.generic.base.ContextMixin):
    def get_vars(self):
        return dict(item_counts={
            'judges': judges.models.Judge.objects.all().count(),
            'prisons': prisons.models.Prison.objects.all().count(),
            'prisoners': prisoners.models.Prisoner.objects.all().count(),
        })

    def get_context_data(self, **kwargs):
        return (super(VarsMixin, self)
                .get_context_data(request=self.request,
                                  is_superuser=api.viewsets.is_superuser(self.request),
                                  **self.get_vars()))


@ui.decorators.class_login_required
class DashboardHomeView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/home.djt.html'


@ui.decorators.class_login_required
class DashboardSearchResultsView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/search_results.djt.html'

    def get_context_data(self, **kwargs):
        return (super(DashboardSearchResultsView, self)
                .get_context_data(request=self.request, **kwargs))


@ui.decorators.class_login_required
class JudgeListView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/judge_list.djt.html'


@ui.decorators.class_login_required
class NewJudgeView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/judge.djt.html'


@ui.decorators.class_login_required
class JudgeDetailView(VarsMixin, django.views.generic.DetailView):
    queryset = judges.models.Judge.objects.all()
    template_name = 'ui/dashboard/judge.djt.html'


@ui.decorators.class_login_required
class PrisonListView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/prison_list.djt.html'


@ui.decorators.class_login_required
class NewPrisonView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/prison.djt.html'


@ui.decorators.class_login_required
class PrisonDetailView(VarsMixin, django.views.generic.DetailView):
    queryset = prisons.models.Prison.objects.all()
    template_name = 'ui/dashboard/prison.djt.html'


@ui.decorators.class_login_required
class PrisonerListView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/prisoner_list.djt.html'


@ui.decorators.class_login_required
class NewPrisonerView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/prisoner.djt.html'


@ui.decorators.class_login_required
class PrisonerDetailView(VarsMixin, django.views.generic.DetailView):
    queryset = prisoners.models.Prisoner.objects.all()
    template_name = 'ui/dashboard/prisoner.djt.html'


@ui.decorators.class_login_required
class ReportListView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/report_list.djt.html'


@ui.decorators.class_login_required
class NewReportView(VarsMixin, django.views.generic.TemplateView):
    template_name = 'ui/dashboard/report.djt.html'


@ui.decorators.class_login_required
class ReportDetailView(VarsMixin, django.views.generic.DetailView):
    queryset = report.models.Report.objects.all()
    template_name = 'ui/dashboard/report.djt.html'
