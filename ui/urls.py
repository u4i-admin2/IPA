from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_change, password_change_done

import ui.views


dashboard_patterns = [
    url('^$',
        ui.views.DashboardHomeView.as_view(),
        name='home'),

    url('^search/$',
        ui.views.DashboardSearchResultsView.as_view(),
        name='search_results'),

    url('^judges/$',
        ui.views.JudgeListView.as_view(),
        name='judge_list'),

    url('^judges/new/$',
        ui.views.NewJudgeView.as_view(),
        name='new_judge'),

    url(r'^judges/(?P<pk>\d+)/$',
        ui.views.JudgeDetailView.as_view(),
        name='judge_detail'),

    url('^prisons/$',
        ui.views.PrisonListView.as_view(),
        name='prison_list'),

    url('^prisons/new/$',
        ui.views.NewPrisonView.as_view(),
        name='new_prison'),

    url(r'^prisons/(?P<pk>\d+)/$',
        ui.views.PrisonDetailView.as_view(),
        name='prison_detail'),

    url('^prisoners/$',
        ui.views.PrisonerListView.as_view(),
        name='prisoner_list'),

    url('^prisoners/new/$',
        ui.views.NewPrisonerView.as_view(),
        name='new_prisoner'),

    url(r'^prisoners/(?P<pk>\d+)/$',
        ui.views.PrisonerDetailView.as_view(),
        name='prisoner_detail'),

    url('^reports/$',
        ui.views.ReportListView.as_view(),
        name='report_list'),

    url('^reports/new/$',
        ui.views.NewReportView.as_view(),
        name='new_report'),

    url(r'^reports/(?P<pk>\d+)/$',
        ui.views.ReportDetailView.as_view(),
        name='report_detail'),
]


users_patterns = [
    url('^login/$',
        login,
        {
            'template_name': 'ui/users/login.djt.html'
        },
        name='login'),

    url('^logout/$',
        logout,
        {
            'template_name': 'ui/users/logout.djt.html'
        },
        name='logout'),

    url('^password/$',
        password_change,
        {
            'template_name': 'ui/users/password_change.djt.html',
            'post_change_redirect': 'ui:users:password_change_done',
        },
        name='password_change'),

    url('^password/done/$',
        password_change_done,
        {
            'template_name': 'ui/users/password_change_done.djt.html',
        },
        name='password_change_done'),
]

urlpatterns = [
    url('^dashboard/',
        include(dashboard_patterns, namespace='dashboard')),

    url('^users/',
        include(users_patterns, namespace='users')),
]
