
import rest_framework.serializers

import api.fields
import core_types.serializers
import judges.models


class SentenceTypeSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:sentencetype-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = judges.models.SentenceType
        fields = core_types.serializers.ChoiceSerializer.Meta.fields + (
            'finality',
        )


class BehaviourTypeSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:behaviourtype-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = judges.models.BehaviourType


class JudicialPositionSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:judicialposition-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = judges.models.JudicialPosition


class CourtAndBranchSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:courtandbranch-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = judges.models.CourtAndBranch


class JudgePositionSerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:judgeposition-detail')
    judge_id = rest_framework.serializers.IntegerField()

    court_and_branch = CourtAndBranchSerializer(
        read_only=True)
    judicial_position = JudicialPositionSerializer(
        read_only=True)

    started_year = api.fields.GregorianYearField()
    started_month = api.fields.GregorianMonthField()
    started_day = api.fields.GregorianDayField()
    started_year_fa = api.fields.FarsiYearField()
    started_month_fa = api.fields.FarsiMonthField()
    started_day_fa = api.fields.FarsiDayField()

    ended_year = api.fields.GregorianYearField()
    ended_month = api.fields.GregorianMonthField()
    ended_day = api.fields.GregorianDayField()
    ended_year_fa = api.fields.FarsiYearField()
    ended_month_fa = api.fields.FarsiMonthField()
    ended_day_fa = api.fields.FarsiDayField()

    class Meta:
        model = judges.models.JudgePosition
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'judge_id',
            'court_and_branch',
            'judicial_position',
            'started_year',
            'started_month',
            'started_day',
            'started_year_fa',
            'started_month_fa',
            'started_day_fa',
            'ended_year',
            'ended_month',
            'ended_day',
            'ended_year_fa',
            'ended_month_fa',
            'ended_day_fa',
        )
        writable_nested_fields = (
            'court_and_branch',
            'judicial_position',
        )


class JudgeQuoteSerializer(core_types.serializers.QuoteSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:judgequote-detail')
    judge_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.QuoteSerializer.Meta):
        model = judges.models.JudgeQuote
        fields = core_types.serializers.QuoteSerializer.Meta.fields + (
            'judge_id',
        )


class JudgeFileSerializer(core_types.serializers.FileSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:judgefile-detail')
    judge_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.FileSerializer.Meta):
        model = judges.models.JudgeFile
        fields = core_types.serializers.FileSerializer.Meta.fields + (
            'judge_id',
            'file_type',
        )


class JudgeTimelineSerializer(core_types.serializers.TimelineSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:judgetimeline-detail')
    judge_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.TimelineSerializer.Meta):
        model = judges.models.JudgeTimeline
        fields = core_types.serializers.TimelineSerializer.Meta.fields + (
            'judge_id',
        )


class JudgeSourceSerializer(core_types.serializers.SourceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:judgesource-detail')
    judge_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.SourceSerializer.Meta):
        model = judges.models.JudgeSource
        fields = core_types.serializers.SourceSerializer.Meta.fields + (
            'judge_id',
        )


class JudgeCommentSerializer(core_types.serializers.CommentSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:judgecomment-detail')
    judge_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.CommentSerializer.Meta):
        model = judges.models.JudgeComment
        fields = core_types.serializers.CommentSerializer.Meta.fields + (
            'judge_id',
        )


class JudgeSummarySerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:judge-detail')

    court_and_branch = CourtAndBranchSerializer(
        allow_null=True,
        read_only=True)

    class Meta:
        model = judges.models.Judge
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'forename_en',
            'forename_fa',
            'surname_en',
            'surname_fa',
            'court_and_branch',
            'judge_type',
            'is_judge',
        )


class JudgeSerializer(JudgeSummarySerializer):
    judicial_position = JudicialPositionSerializer(
        allow_null=True,
        read_only=True)

    birth_city = core_types.serializers.CitySerializer(
        allow_null=True,
        read_only=True)

    birth_province = core_types.serializers.ProvinceSerializer(
        allow_null=True,
        read_only=True)

    ethnicity = core_types.serializers.EthnicitySerializer(
        allow_null=True,
        read_only=True)

    timeline = JudgeTimelineSerializer(
        many=True,
        read_only=True)

    quotes = JudgeQuoteSerializer(
        many=True,
        read_only=True)

    files = JudgeFileSerializer(
        many=True,
        read_only=True)

    positions = JudgePositionSerializer(
        many=True,
        read_only=True)

    sources = JudgeSourceSerializer(
        many=True,
        read_only=True)

    comments = JudgeCommentSerializer(
        many=True,
        read_only=True)

    picture_resized = api.fields.ThumbnailImageField(source='picture')
    picture_200x200 = api.fields.ThumbnailImageField(source='picture', size=(200, 200))

    dob_year = api.fields.GregorianYearField()
    dob_month = api.fields.GregorianMonthField()
    dob_day = api.fields.GregorianDayField()
    dob_year_fa = api.fields.FarsiYearField()
    dob_month_fa = api.fields.FarsiMonthField()
    dob_day_fa = api.fields.FarsiDayField()

    class Meta(JudgeSummarySerializer.Meta):
        fields = JudgeSummarySerializer.Meta.fields + (
            'dob_year',
            'dob_month',
            'dob_day',
            'dob_year_fa',
            'dob_month_fa',
            'dob_day_fa',
            'dob_is_estimate',
            'birth_city',
            'birth_province',
            'ethnicity',
            'biography_en',
            'biography_fa',
            'picture',
            'picture_resized',
            'picture_200x200',
            'is_cleric',
            'judicial_position',
            'quotes',
            'files',
            'timeline',
            'positions',
            'sources',
            'comments',
            'explanation_en',
            'explanation_fa',
            'explanation_aea_en',
            'explanation_aea_fa',
        )
        # See api/serializers.py:ModelSerializer.create().
        writable_nested_fields = (
            'court_and_branch',
            'judicial_position',
            'birth_city',
            'birth_province',
            'ethnicity',
        )

    def get_extra_kwargs(self):
        kwargs = super(JudgeSerializer, self).get_extra_kwargs()
        for field in self.Meta.fields:
            kwargs[field] = {
                'required': False
            }
        kwargs['is_cleric']['allow_null'] = True
        return kwargs
