from rest_framework import filters
from api.viewsets import ModelViewSet

from .models import (
    Report,
    ReportQuote,
    ReportFile,
    ReportSentence,
    ReportComment,
    ReportSource,
    ReportDetention,
    HumanRightViolated
)

from .serializers import (
    ReportSerializer,
    ReportQuoteSerializer,
    ReportFileSerializer,
    ReportSentenceSerializer,
    ReportCommentSerializer,
    ReportSourceSerializer,
    ReportDetentionSerializer,
    HumanRightViolatedSerializer,
)


class ReportQuoteViewSet(ModelViewSet):
    queryset = ReportQuote.objects.all()
    serializer_class = ReportQuoteSerializer


class ReportFileViewSet(ModelViewSet):
    queryset = ReportFile.objects.all()
    serializer_class = ReportFileSerializer


class ReportSentenceViewSet(ModelViewSet):
    queryset = ReportSentence.objects.all()
    serializer_class = ReportSentenceSerializer


class ReportCommentViewSet(ModelViewSet):
    queryset = ReportComment.objects.all()
    serializer_class = ReportCommentSerializer


class ReportSourceViewSet(ModelViewSet):
    queryset = ReportSource.objects.all()
    serializer_class = ReportSourceSerializer


class ReportDetentionViewSet(ModelViewSet):
    queryset = ReportDetention.objects.all()
    serializer_class = ReportDetentionSerializer


class ReportFilterBackend(filters.BaseFilterBackend):
    """
    Implement various custom filters for the Reports
    """
    def filter_queryset(self, request, queryset, view):

        has_comments = request.GET.get('has_comments')
        if has_comments:
            has_comments = not (has_comments == '1')
            queryset = queryset.filter(comments__comment__isnull=has_comments)

        return queryset


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = ModelViewSet.filter_backends + [
        ReportFilterBackend,
    ]


class HumanRightViolatedViewSet(ModelViewSet):
    queryset = HumanRightViolated.objects.all()
    serializer_class = HumanRightViolatedSerializer


VIEWSETS = [
    ReportViewSet,
    ReportQuoteViewSet,
    ReportFileViewSet,
    ReportSentenceViewSet,
    ReportCommentViewSet,
    ReportSourceViewSet,
    ReportDetentionViewSet,
    HumanRightViolatedViewSet,
]
