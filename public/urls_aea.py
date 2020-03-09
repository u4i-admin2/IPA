from django.conf.urls import url
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap
from ipa import sitemaps

from public import views
from public import views_v2

aea_sitemaps = {
    'FirstLevel': sitemaps.FirstLevel,
    'Prisons': sitemaps.PrisonsSitemap,
    'Judges': sitemaps.JudgesSitemap
}

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': aea_sitemaps},
        name='sitemap'),
    url(r'^$', cache_page(60 * 60)(views_v2.Home.as_view()), name='homepage'),

    url(r'^prison/$', cache_page(60 * 60)(views.AeaPrisons.as_view()), name='prisons'),
    url(r'^prison/(?P<pk>[\d]+)/$', cache_page(60 * 60)(views.AeaPrisonView.as_view()), name='prison'),

    url(
        r'^judge/$',
        cache_page(60 * 60)(views.AeaJudges.as_view()),
        name='judges',
    ),
    url(
        r'^judge/(?P<pk>[\d]+)/$',
        cache_page(60 * 60)(views_v2.JudgeAea.as_view()),
        name='judge',
    ),

    url(r'^search/$', cache_page(60 * 60)(views.AeaSearch.as_view()), name='search'),

    # REST endpoints
    url(r'^report-summary/(?P<pk>[\d]+)/$',
        cache_page(60 * 60)(views.ReportSummaryView.as_view()),
        name='report-summary'),
    url(r'^search-prisons/$',
        cache_page(60 * 60)(views.AeaSearchPrisons.as_view({'get': 'list'})),
        name='search-prisons'),
    url(r'^search-judges/$',
        cache_page(60 * 60)(views.AeaSearchJudges.as_view({'get': 'list'})),
        name='search-judges'),

    url(r'^about/$',
        cache_page(60 * 60)(views.PageDetail.as_view()),
        name='about'),

    url(r'^about/(?P<slug>[\w-]+)/$',
        cache_page(60 * 60)(views.PageDetail.as_view()),
        name='about_page'),
]
