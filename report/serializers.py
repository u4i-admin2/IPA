from rest_framework import serializers

from .models import (
    Report,
    ReportQuote,
    ReportFile,
    ReportSentence,
    ReportSentenceBehaviour,
    ReportComment,
    ReportSource,
    ReportDetention,
    HumanRightViolated
)
from core_types.serializers import (
    QuoteSerializer,
    FileSerializer,
    ChoiceSerializer,
    CommentSerializer,
    PublishableModelSerializer,
    CitySerializer,
    PUBLISHABLE_FIELDS
)
from prisons.serializers import (
    PrisonSummarySerializer,
)
from judges.serializers import (
    BehaviourTypeSerializer,
    JudgeSummarySerializer,
    CourtAndBranchSerializer,
)
from prisoners.serializers import (
    DomesticLawViolatedSerializer,
    InternationalLawViolatedSerializer
)
from api.fields import (
    GregorianDayField,
    GregorianMonthField,
    GregorianYearField,
    FarsiDayField,
    FarsiMonthField,
    FarsiYearField
)


class ReportQuoteSerializer(QuoteSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:reportquote-detail')
    report_id = serializers.IntegerField()

    class Meta(QuoteSerializer.Meta):
        model = ReportQuote
        fields = QuoteSerializer.Meta.fields + (
            'report_id',
        )


class ReportFileSerializer(FileSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:reportfile-detail')
    report_id = serializers.IntegerField()

    class Meta(FileSerializer.Meta):
        model = ReportFile
        fields = FileSerializer.Meta.fields + (
            'report_id',
            'file_type',
        )


class HumanRightViolatedSerializer(ChoiceSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:humanrightviolated-detail')

    class Meta(ChoiceSerializer.Meta):
        model = HumanRightViolated


class ReportSummarySerializer(PublishableModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:report-detail')

    class Meta:
        model = Report
        fields = PUBLISHABLE_FIELDS + (
            'picture',
            'victim_count')


class ReportSentenceSerializer(PublishableModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:reportsentence-detail')
    sentence_id = serializers.IntegerField(source='id')
    report = ReportSummarySerializer(read_only=True)
    judge = JudgeSummarySerializer(read_only=True)
    judge_court_and_branch = CourtAndBranchSerializer()

    class Meta:
        model = ReportSentence
        fields = PUBLISHABLE_FIELDS + (
            'sentence_id',
            'execution',
            'flogging',
            'amputation',
            'report',
            'judge',
            'judge_court_and_branch')


class ReportCommentSerializer(CommentSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:reportcomment-detail')
    prisoner_id = serializers.IntegerField()

    class Meta(CommentSerializer.Meta):
        model = ReportComment
        fields = CommentSerializer.Meta.fields + (
            'prisoner_id',
            'report_id',
        )


class ReportSourceSerializer(PublishableModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:reportsource-detail')
    report = ReportSummarySerializer(read_only=True)

    class Meta:
        model = ReportSource
        fields = PUBLISHABLE_FIELDS + (
            'report',
            'name',
            'link',
            'description',
            'related_fields')


class ReportDetentionSerializer(PublishableModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:reportdetention-detail')
    report_id = serializers.IntegerField()

    prison = PrisonSummarySerializer(
        allow_null=True,
        read_only=True)

    detention_year = GregorianYearField()
    detention_month = GregorianMonthField()
    detention_day = GregorianDayField()
    detention_year_fa = FarsiYearField()
    detention_month_fa = FarsiMonthField()
    detention_day_fa = FarsiDayField()

    class Meta:
        model = ReportDetention
        fields = PUBLISHABLE_FIELDS + (
            'report_id',
            'prison',
            'detention_type',
            'detention_year',
            'detention_month',
            'detention_day',
            'detention_year_fa',
            'detention_month_fa',
            'detention_day_fa',
            'detention_is_approx',
        )
        writable_nested_fields = (
            'prison',
        )


class ReportSentenceBehaviourSerializer(PublishableModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:reportsentencebehaviour-detail')
    judge_behaviour = BehaviourTypeSerializer()
    report_sentence = ReportSentenceSerializer()

    class Meta:
        model = ReportSentenceBehaviour
        fields = PUBLISHABLE_FIELDS + (
            'description',
            'description_fa',
            'description_en',
            'judge_behaviour',
            'report_sentence'
        )
        writable_nested_fields = (
            'judge_behaviour',
            'report_sentence',
        )


class ReportSerializer(PublishableModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:report-detail')

    city = CitySerializer(
        allow_null=True,
        read_only=True)
    domestic_law_violated_objs = DomesticLawViolatedSerializer(
        many=True,
        source='domestic_law_violated',
        read_only=True)
    international_law_violated_objs = InternationalLawViolatedSerializer(
        many=True,
        source='international_law_violated',
        read_only=True)
    human_right_violated_objs = HumanRightViolatedSerializer(
        many=True,
        source='human_right_violated',
        read_only=True)

    class Meta:
        model = Report
        fields = PUBLISHABLE_FIELDS + (
            'picture',
            'abstract_text',
            'abstract_text_en',
            'abstract_text_fa',
            'victim_count',
            'city',
            'charged_with',
            'domestic_law_violated_objs',
            'international_law_violated_objs',
            'human_right_violated_objs',
            'explanation_en',
            'explanation_fa'
        )
