from django.db.models import Q
from django.conf import settings
from rest_framework.settings import api_settings

from django.http import HttpResponse

from rest_framework.filters import BaseFilterBackend
import boto3

from api.viewsets import (
    ModelViewSet,
    ChoiceViewSet,
    ImageUploadViewSet,
    TagListViewSet
)
from prisoners.renderers import PrisonerCsvRenderer
from prisoners.models import (
    Prisoner,
    PrisonerQuote,
    PrisonerFile,
    PrisonerRelationship,
    PrisonerAffiliation,
    PrisonerArrest,
    PrisonerDetention,
    PrisonerSentence,
    PrisonerTimeline,
    RelationshipType,
    Organisation,
    ActivityPersecutedFor,
    ChargedWith,
    CaseId,
    DomesticLawViolated,
    InternationalLawViolated,
    DetentionStatus,
    PrisonTreatment,
    PrisonerSource,
    PrisonerComment,
    SentenceBehaviour
)
from prisoners.serializers import (
    PrisonerSerializer,
    PrisonerQuoteSerializer,
    PrisonerFileSerializer,
    PrisonerRelationshipSerializer,
    PrisonerAffiliationSerializer,
    PrisonerArrestSerializer,
    PrisonerDetentionSerializer,
    PrisonerSentenceSerializer,
    PrisonerTimelineSerializer,
    RelationshipTypeSerializer,
    OrganisationSerializer,
    ActivityPersecutedForSerializer,
    ChargedWithSerializer,
    CaseIdSerializer,
    DomesticLawViolatedSerializer,
    InternationalLawViolatedSerializer,
    DetentionStatusSerializer,
    PrisonTreatmentSerializer,
    PrisonerSourceSerializer,
    PrisonerCommentSerializer,
    SentenceBehaviourSerializer,
)


class PrisonerQuoteViewSet(ModelViewSet):
    queryset = PrisonerQuote.objects.all()
    serializer_class = PrisonerQuoteSerializer


class PrisonerFileViewSet(ModelViewSet):
    queryset = PrisonerFile.objects.all()
    serializer_class = PrisonerFileSerializer


class PrisonerRelationshipViewSet(ModelViewSet):
    queryset = PrisonerRelationship.objects.all()
    serializer_class = PrisonerRelationshipSerializer


class PrisonerAffiliationViewSet(ModelViewSet):
    queryset = PrisonerAffiliation.objects.all()
    serializer_class = PrisonerAffiliationSerializer


class PrisonerArrestViewSet(ModelViewSet):
    queryset = (
        PrisonerArrest.objects.all().prefetch_related(
            'case_id'))
    serializer_class = PrisonerArrestSerializer


class PrisonerDetentionViewSet(ModelViewSet):
    queryset = PrisonerDetention.objects.all()
    serializer_class = PrisonerDetentionSerializer


class PrisonerSentenceViewSet(ModelViewSet):
    queryset = PrisonerSentence.objects.all()
    serializer_class = PrisonerSentenceSerializer


class PrisonerTimelineViewSet(ModelViewSet):
    queryset = PrisonerTimeline.objects.all()
    serializer_class = PrisonerTimelineSerializer


class RelationshipTypeViewSet(ChoiceViewSet):
    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer


class OrganisationViewSet(ChoiceViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class ActivityPersecutedForViewSet(ChoiceViewSet):
    queryset = ActivityPersecutedFor.objects.all()
    serializer_class = ActivityPersecutedForSerializer


class ChargedWithViewSet(ChoiceViewSet):
    queryset = ChargedWith.objects.all()
    serializer_class = ChargedWithSerializer


class CaseIdViewSet(ChoiceViewSet):
    queryset = CaseId.objects.all()
    serializer_class = CaseIdSerializer


class DomesticLawViolatedViewSet(ChoiceViewSet):
    queryset = DomesticLawViolated.objects.all()
    serializer_class = DomesticLawViolatedSerializer


class InternationalLawViolatedViewSet(ChoiceViewSet):
    queryset = InternationalLawViolated.objects.all()
    serializer_class = InternationalLawViolatedSerializer


class DetentionStatusViewSet(ChoiceViewSet):
    queryset = DetentionStatus.objects.all()
    serializer_class = DetentionStatusSerializer


class PrisonTreatmentViewSet(ChoiceViewSet):
    queryset = PrisonTreatment.objects.all()
    serializer_class = PrisonTreatmentSerializer


class PrisonerSourceViewSet(ModelViewSet):
    queryset = PrisonerSource.objects.all()
    serializer_class = PrisonerSourceSerializer


class PrisonerCommentViewSet(ModelViewSet):
    queryset = PrisonerComment.objects.all()
    serializer_class = PrisonerCommentSerializer


class SentenceBehaviourViewSet(ModelViewSet):
    queryset = SentenceBehaviour.objects.all()
    serializer_class = SentenceBehaviourSerializer


class PrisonerFilterBackend(BaseFilterBackend):
    """
    Implement various custom filters for the Prisoner collection using criteria
    from issue #89.
    """
    def filter_queryset(self, request, queryset, view):
        is_detained = request.GET.get('is_detained')

        if is_detained and int(is_detained) == 1:
            # actually released
            queryset = queryset.filter(detention_status__detained=False)
        if is_detained and int(is_detained) == 0:
            # actually detained
            queryset = queryset.filter(detention_status__detained=True)

        religion = request.GET.get('religion')
        if religion:
            queryset = queryset.filter(Q(religion__name_en__icontains=religion) |
                                       Q(religion__name_fa__icontains=religion))

        ethnicity = request.GET.get('ethnicity')
        if ethnicity:
            queryset = queryset.filter(Q(ethnicity__name_en__icontains=ethnicity) |
                                       Q(ethnicity__name_fa__icontains=ethnicity))

        gender = request.GET.get('gender')
        if gender:
            queryset = queryset.filter(gender__iexact=gender)

        has_comments = request.GET.get('has_comments')
        if has_comments:
            has_comments = not (has_comments == '1')
            queryset = queryset.filter(comments__comment__isnull=has_comments)

        persecuted_for = request.GET.get('activity_persecuted_for')
        if persecuted_for:
            queryset = queryset.filter(
                Q(arrests__activity_persecuted_for__name_en__icontains=persecuted_for) |
                Q(arrests__activity_persecuted_for__name_fa__icontains=persecuted_for))

        arrest_year_min = request.GET.get('arrest_year_min')
        if arrest_year_min and arrest_year_min.isdigit():
            queryset = (queryset
                        .filter(arrests__arrest_year__gte=int(arrest_year_min, 10)))

        arrest_year_max = request.GET.get('arrest_year_max')
        if arrest_year_max and arrest_year_max.isdigit():
            queryset = (queryset
                        .filter(arrests__arrest_year__lte=int(arrest_year_max, 10)))

        sentence_min = request.GET.get('sentence_min')

        if sentence_min and sentence_min.isdigit():
            ids = PrisonerSentence.objects.filter(
                sentence_years__gte=int(sentence_min, 0)).values_list(
                'arrest__prisoner_id')
            queryset = (queryset.filter(id__in=ids))

        sentence_max = request.GET.get('sentence_max')

        if sentence_max and sentence_max.isdigit():
            ids = PrisonerSentence.objects.filter(
                sentence_years__lte=int(sentence_max, 100)).values_list(
                'arrest__prisoner_id')
            queryset = (queryset.filter(id__in=ids))

        sentence = request.GET.get('sentence')
        if sentence and sentence == 'life':
            ids = PrisonerSentence.objects.filter(
                life=True).values_list('arrest__prisoner_id')
            queryset = (queryset.filter(id__in=ids))

        if sentence and sentence == 'exiled':
            ids = PrisonerSentence.objects.filter(
                exiled=True).values_list('arrest__prisoner_id')
            queryset = (queryset.filter(id__in=ids))

        if sentence and sentence == 'execution':
            ids = PrisonerSentence.objects.filter(
                death_penalty=True).values_list('arrest__prisoner_id')
            queryset = (queryset.filter(id__in=ids))

        featured = request.GET.get('featured')
        if featured:
            queryset = (queryset.filter(featured=True))

        return queryset


class PrisonerViewSet(ModelViewSet):

    queryset = Prisoner.prefetch_queryset(
        Prisoner.objects.all())
    serializer_class = PrisonerSerializer
    filter_backends = ModelViewSet.filter_backends + [
        PrisonerFilterBackend,
    ]
    search_fields = (
        'forename_en',
        'forename_fa',
        'surname_en',
        'surname_fa',
    )


class PrisonerCSV(PrisonerViewSet):
    base_name = 'csv'
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + \
        [PrisonerCsvRenderer]

    def list(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        if(settings.AWS_ACCESS_KEY_ID is None or
                settings.AWS_SECRET_ACCESS_KEY is None or
                settings.AWS_STORAGE_BUCKET_NAME is None):
            filename = '{}/{}'.format(settings.MEDIA_ROOT, settings.PRISONERS_CSV_FILE_KEY_NAME)
            with open(filename, 'r') as csvfile:
                content = csvfile.read()
        else:
            s3_res = boto3.resource(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                config=boto3.session.Config(signature_version='s3v4'),
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            obj = s3_res.Object(settings.AWS_STORAGE_BUCKET_NAME, settings.PRISONERS_CSV_FILE_KEY_NAME)
            content = obj.get()['Body'].read()

        response.write(content)
        response['Content-Disposition'] = "attachment; filename=\"prisoners.csv\""
        response['Content-Type'] = "text/html; charset=utf-8"

        return response


class PrisonerPictureViewSet(ImageUploadViewSet):
    queryset = Prisoner.objects.all()
    base_name = 'prisonerpictures'
    prefix = 'prisoners/pictures'


class PrisonerTagListViewSet(TagListViewSet):
    MODULE_NAME = 'prisoners.models'
    base_name = 'prisonertaglist'


VIEWSETS = [
    ActivityPersecutedForViewSet,
    CaseIdViewSet,
    ChargedWithViewSet,
    DetentionStatusViewSet,
    DomesticLawViolatedViewSet,
    InternationalLawViolatedViewSet,
    OrganisationViewSet,
    PrisonTreatmentViewSet,
    PrisonerAffiliationViewSet,
    PrisonerArrestViewSet,
    PrisonerCommentViewSet,
    PrisonerDetentionViewSet,
    PrisonerFileViewSet,
    PrisonerPictureViewSet,
    PrisonerQuoteViewSet,
    PrisonerRelationshipViewSet,
    PrisonerSentenceViewSet,
    PrisonerSourceViewSet,
    PrisonerTagListViewSet,
    PrisonerTimelineViewSet,
    PrisonerViewSet,
    RelationshipTypeViewSet,
    SentenceBehaviourViewSet,
    PrisonerCSV,
]
