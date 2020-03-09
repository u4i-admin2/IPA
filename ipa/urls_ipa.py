from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from public.views import Robots

from ipa.error_handlers import * # noqa: 401

admin.site.site_header = 'United for Iran Admin'
admin.site.site_title = 'United for Iran Admin'


urlpatterns = [
    url(r'^u-admin/',
        include(admin.site.urls)),

    url('^api/',
        include('api.urls', namespace='api')),

    url('',
        include('ui.urls', namespace='ui')),

    url(r'^robots.txt$',
        Robots.as_view(content_type='text/plain'),
        name='robots.txt'),

    url(r'^accounts/', include('allauth.urls')),
]

# multilingual patterns (prefixed en/fa)
urlpatterns += i18n_patterns(
    url(r'', include('public.urls_ipa', namespace='public')),
)

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += (
    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
