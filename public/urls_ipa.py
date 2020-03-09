from django.conf.urls import url
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap
from ipa import sitemaps

from public import views
from public import views_v2

ipa_sitemaps = {
    'FirstLevel': sitemaps.FirstLevel,
    'Prisoners': sitemaps.PrisonersSitemap,
    'Prisons': sitemaps.PrisonsSitemap,
    'Judges': sitemaps.JudgesSitemap
}

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': ipa_sitemaps},
        name='sitemap'),
    url(r'^$', cache_page(60 * 60)(views_v2.Home.as_view()), name='homepage'),

    url(r'^prison/$', cache_page(60 * 60)(views.Prisons.as_view()), name='prisons'),
    url(r'^prison/(?P<pk>[\d]+)/$', cache_page(60 * 60)(views.PrisonView.as_view()), name='prison'),

    url(r'^prisoner/$', cache_page(60 * 60)(views.Prisoners.as_view()), name='prisoners'),
    url(r'^prisoner/(?P<pk>[\d]+)/$', cache_page(60 * 60)(views.PrisonerView.as_view()), name='prisoner'),

    url(
        r'^judge/$',
        cache_page(60 * 60)(views.Judges.as_view()),
        name='judges',
    ),
    url(
        r'^judge/(?P<pk>[\d]+)/$',
        cache_page(60 * 60)(views_v2.JudgeIpa.as_view()),
        name='judge'
    ),

    url(r'^search/$', cache_page(60 * 60)(views.Search.as_view()), name='search'),

    # REST endpoints
    url(r'^prisoner-summary/(?P<pk>[\d]+)/$',
        cache_page(60 * 60)(views.PrisonerSummaryView.as_view()),
        name='prisoner-summary'),
    url(r'^judge/(?P<judge_id>[\d]+)/sentences/$',
        cache_page(60 * 60)(views.SentencesByJudgeView.as_view()),
        name='judge-sentences'),
    url(r'^search-prisoners/$',
        cache_page(60 * 60)(views.SearchPrisoners.as_view({'get': 'list'})),
        name='search-prisoners'),
    url(r'^search-prisons/$',
        cache_page(60 * 60)(views.SearchPrisons.as_view({'get': 'list'})),
        name='search-prisons'),
    url(r'^search-judges/$',
        cache_page(60 * 60)(views.SearchJudges.as_view({'get': 'list'})),
        name='search-judges'),

    url(r'^about/$',
        cache_page(60 * 60)(views.PageDetail.as_view()),
        name='about'),

    url(r'^about/(?P<slug>[\w-]+)/$',
        cache_page(60 * 60)(views.PageDetail.as_view()),
        name='about_page'),
]
