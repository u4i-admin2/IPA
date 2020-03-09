"""
This builds the list of exported API urls up by examining viewsets registered
via api/components.py. Read that file for an example.
"""

import rest_framework.routers

import api.search
import api.viewsets


class Router(rest_framework.routers.DefaultRouter):
    root_view_name = 'root'


router = Router()
router.register('search', api.search.WatsonSearchViewSet,
                base_name='search')

for app_name, viewsets in api.viewsets.VIEWSETS:
    for viewset in viewsets:
        base_name = getattr(viewset, 'base_name', None)
        if not base_name:
            base_name = str(viewset.queryset.model.__name__.lower())

        prefix = getattr(viewset, 'prefix', None)
        if not prefix:
            prefix = '%s/%s' % (app_name, base_name)

        router.register(prefix, viewset, base_name=base_name)

urlpatterns = router.urls
