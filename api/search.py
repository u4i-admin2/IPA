
from django.utils.translation import ugettext_lazy as _
import rest_framework.exceptions
import rest_framework.response
import rest_framework.viewsets
from watson import search as watson
from core_types import models as core_types_models

SERIALIZERS = {}


def register(model, serializer):
    """
    Register a model for the search engine.
    """
    SERIALIZERS[model] = serializer
    watson.register(model)


class WatsonSearchViewSet(rest_framework.viewsets.ViewSet):
    """
    Watson searcher; hides is_published=False if the user isn't logged in.
    """
    base_name = 'search'
    param_name = 'q'

    def convert_result(self, model):
        """
        Convert a model into JSON, using the model's associated serializer
        located via api.components.SERIALIZERS.
        """
        model_class = type(model)
        serializer_class = SERIALIZERS[model_class]
        serializer = serializer_class(model, context={
            'request': self.request
        })
        mapped = serializer.data
        mapped['type'] = model_class.__name__.lower()
        return mapped

    def build_excludes(self):
        """
        Return a list of querysets that should not be matched by Watson. If the
        requesting user is not logged in, then this filters all
        is_published=False models.
        """
        excludes = []
        if self.request.user is None:
            for model in watson.get_registered_models():
                if issubclass(model, core_types_models.PublishableMixin):
                    excludes.append(model.objects.filter(is_published=False))
        return excludes

    def list(self, request):
        """
        Respond to list() requests by running a Watson search, then using
        api.urls.API_VIEW_MODULES to map each matched model back to its
        equivalent serializer.
        """
        query = request.GET.get(self.param_name)
        if not query:
            msg = _('You must specify %r parameter.' % (self.param_name,))
            raise rest_framework.exceptions.ParseError(msg)

        ids_by_type = {}
        results = (watson.search(
            query, exclude=self.build_excludes()).prefetch_related(
            'object'))[:400]

        for result in results:
            model = result.object
            if model:
                ids_by_type.setdefault(type(model), []).append(model.id)

        prefetched_results = []
        for model_class, ids in ids_by_type.iteritems():
            qs = model_class.objects.filter(pk__in=ids)
            qs = model_class.prefetch_queryset(qs)
            prefetched_results.extend(qs)

        json = map(self.convert_result, prefetched_results)
        return rest_framework.response.Response(json)
