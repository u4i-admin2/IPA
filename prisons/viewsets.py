
import api.viewsets
import prisons.models
import prisons.serializers


class PrisonQuoteViewSet(api.viewsets.ModelViewSet):
    queryset = prisons.models.PrisonQuote.objects.all()
    serializer_class = prisons.serializers.PrisonQuoteSerializer


class PrisonFacilityLinkViewSet(api.viewsets.ModelViewSet):
    queryset = prisons.models.PrisonFacilityLink.objects.all()
    serializer_class = prisons.serializers.PrisonFacilityLinkSerializer


class PrisonFileViewSet(api.viewsets.ModelViewSet):
    queryset = prisons.models.PrisonFile.objects.all()
    serializer_class = prisons.serializers.PrisonFileSerializer


class PrisonTimelineViewSet(api.viewsets.ModelViewSet):
    queryset = prisons.models.PrisonTimeline.objects.all()
    serializer_class = prisons.serializers.PrisonTimelineSerializer


class PrisonFacilityViewSet(api.viewsets.ChoiceViewSet):
    queryset = prisons.models.PrisonFacility.objects.all()
    serializer_class = prisons.serializers.PrisonFacilitySerializer


class PrisonSourceViewSet(api.viewsets.ModelViewSet):
    queryset = prisons.models.PrisonSource.objects.all()
    serializer_class = prisons.serializers.PrisonSourceSerializer


class PrisonCommentViewSet(api.viewsets.ModelViewSet):
    queryset = prisons.models.PrisonComment.objects.all()
    serializer_class = prisons.serializers.PrisonCommentSerializer


class PrisonViewSet(api.viewsets.ModelViewSet):
    queryset = prisons.models.Prison.prefetch_queryset(
        prisons.models.Prison.objects.all())
    serializer_class = prisons.serializers.PrisonSerializer
    search_fields = (
        'name_en',
        'name_fa',
    )


class PrisonPictureViewSet(api.viewsets.ImageUploadViewSet):
    queryset = prisons.models.Prison.objects.all()
    base_name = 'prisonpictures'
    prefix = 'prisons/pictures'


class PrisonTagListViewSet(api.viewsets.TagListViewSet):
    MODULE_NAME = 'prisons.models'
    base_name = 'prisontaglist'


VIEWSETS = [
    PrisonCommentViewSet,
    PrisonFacilityViewSet,
    PrisonFacilityLinkViewSet,
    PrisonFileViewSet,
    PrisonQuoteViewSet,
    PrisonSourceViewSet,
    PrisonTagListViewSet,
    PrisonTimelineViewSet,
    PrisonPictureViewSet,
    PrisonViewSet,
]
