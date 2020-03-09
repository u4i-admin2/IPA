from rest_framework import filters

from api.viewsets import ModelViewSet
from .models import FeaturedNews
from .serializers import FeaturedNewsSerializer


class FeaturedNewsFilterBackend(filters.BaseFilterBackend):
    """
    Implement various custom filters for featured news
    """
    def filter_queryset(self, request, queryset, view):

        featured = request.GET.get('featured')
        if featured:
            queryset = (queryset.filter(featured=True))

        return queryset


class FeaturedNewsViewSet(ModelViewSet):

    queryset = FeaturedNews.published_objects.all()
    serializer_class = FeaturedNewsSerializer

    filter_backends = ModelViewSet.filter_backends + [
        FeaturedNewsFilterBackend,
    ]


VIEWSETS = [
    FeaturedNewsViewSet,
]
