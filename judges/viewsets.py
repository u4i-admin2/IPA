
import api.viewsets
import judges.models
import judges.serializers


class SentenceTypeViewSet(api.viewsets.ChoiceViewSet):
    queryset = (judges.models.SentenceType.objects.all()
                .prefetch_related('created_by')
                .prefetch_related('updated_by'))
    serializer_class = judges.serializers.SentenceTypeSerializer


class BehaviourTypeViewSet(api.viewsets.ChoiceViewSet):
    queryset = (judges.models.BehaviourType.objects.all()
                .prefetch_related('created_by')
                .prefetch_related('updated_by'))
    serializer_class = judges.serializers.BehaviourTypeSerializer


class JudicialPositionViewSet(api.viewsets.ChoiceViewSet):
    queryset = (judges.models.JudicialPosition.objects.all()
                .prefetch_related('created_by')
                .prefetch_related('updated_by'))
    serializer_class = judges.serializers.JudicialPositionSerializer


class CourtAndBranchViewSet(api.viewsets.ChoiceViewSet):
    queryset = (judges.models.CourtAndBranch.objects.all()
                .prefetch_related('created_by')
                .prefetch_related('updated_by'))
    serializer_class = judges.serializers.CourtAndBranchSerializer


class JudgeTimelineViewSet(api.viewsets.ModelViewSet):
    queryset = (judges.models.JudgeTimeline.objects.all()
                .prefetch_related('created_by')
                .prefetch_related('updated_by'))
    serializer_class = judges.serializers.JudgeTimelineSerializer


class JudgePositionViewSet(api.viewsets.ModelViewSet):
    queryset = (judges.models.JudgePosition.objects.all()
                .prefetch_related('created_by')
                .prefetch_related('updated_by')
                .prefetch_related('court_and_branch')
                .prefetch_related('judicial_position'))
    serializer_class = judges.serializers.JudgePositionSerializer


class JudgeSourceViewSet(api.viewsets.ModelViewSet):
    queryset = judges.models.JudgeSource.objects.all()
    serializer_class = judges.serializers.JudgeSourceSerializer


class JudgeQuoteViewSet(api.viewsets.ModelViewSet):
    queryset = judges.models.JudgeQuote.objects.all()
    serializer_class = judges.serializers.JudgeQuoteSerializer


class JudgeFileViewSet(api.viewsets.ModelViewSet):
    queryset = judges.models.JudgeFile.objects.all()
    serializer_class = judges.serializers.JudgeFileSerializer


class JudgeCommentViewSet(api.viewsets.ModelViewSet):
    queryset = judges.models.JudgeComment.objects.all()
    serializer_class = judges.serializers.JudgeCommentSerializer


class JudgeViewSet(api.viewsets.ModelViewSet):
    queryset = judges.models.Judge.prefetch_queryset(
        judges.models.Judge.objects.all())
    serializer_class = judges.serializers.JudgeSerializer
    search_fields = (
        'forename_en',
        'forename_fa',
        'surname_en',
        'surname_fa',
    )


class JudgePictureViewSet(api.viewsets.ImageUploadViewSet):
    queryset = judges.models.Judge.objects.all()
    base_name = 'judgepictures'
    prefix = 'judges/pictures'


class JudgeTagListViewSet(api.viewsets.TagListViewSet):
    MODULE_NAME = 'judges.models'
    base_name = 'judgetaglist'


VIEWSETS = [
    BehaviourTypeViewSet,
    CourtAndBranchViewSet,
    JudgeCommentViewSet,
    JudgeFileViewSet,
    JudgePictureViewSet,
    JudgePositionViewSet,
    JudgeQuoteViewSet,
    JudgeSourceViewSet,
    JudgeTagListViewSet,
    JudgeTimelineViewSet,
    JudgeViewSet,
    JudicialPositionViewSet,
    SentenceTypeViewSet,
]
