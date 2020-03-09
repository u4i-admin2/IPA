
import rest_framework.serializers

import api.fields
import core_types.serializers
import prisons.models


class PrisonQuoteSerializer(core_types.serializers.QuoteSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonquote-detail')
    prison_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.QuoteSerializer.Meta):
        model = prisons.models.PrisonQuote
        fields = core_types.serializers.QuoteSerializer.Meta.fields + (
            'prison_id',
        )


class PrisonFacilityLinkSerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonfacilitylink-detail')
    prison_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.PublishableModelSerializer.Meta):
        model = prisons.models.PrisonFacilityLink
        fields = core_types.serializers.PublishableModelSerializer.Meta.fields + (
            'prison_id',
            'facility',
            'description_en',
            'description_fa',
        )


class PrisonFileSerializer(core_types.serializers.FileSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonfile-detail')
    prison_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.FileSerializer.Meta):
        model = prisons.models.PrisonFile
        fields = core_types.serializers.FileSerializer.Meta.fields + (
            'prison_id',
            'file_type',
        )


class PrisonTimelineSerializer(core_types.serializers.TimelineSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisontimeline-detail')
    prison_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.TimelineSerializer.Meta):
        model = prisons.models.PrisonTimeline
        fields = core_types.serializers.TimelineSerializer.Meta.fields + (
            'prison_id',
        )


class PrisonFacilitySerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonfacility-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisons.models.PrisonFacility


class PrisonSourceSerializer(core_types.serializers.SourceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonsource-detail')
    prison_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.SourceSerializer.Meta):
        model = prisons.models.PrisonSource
        fields = core_types.serializers.SourceSerializer.Meta.fields + (
            'prison_id',
        )


class PrisonCommentSerializer(core_types.serializers.CommentSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisoncomment-detail')
    prison_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.CommentSerializer.Meta):
        model = prisons.models.PrisonComment
        fields = core_types.serializers.CommentSerializer.Meta.fields + (
            'prison_id',
        )


class PrisonSummarySerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prison-detail')

    class Meta:
        model = prisons.models.Prison
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'name_en',
            'name_fa',
        )


class PrisonSerializer(PrisonSummarySerializer):
    quotes = PrisonQuoteSerializer(
        many=True,
        read_only=True)

    files = PrisonFileSerializer(
        many=True,
        read_only=True)

    timeline = PrisonTimelineSerializer(
        many=True,
        read_only=True)

    sources = PrisonSourceSerializer(
        many=True,
        read_only=True)

    comments = PrisonCommentSerializer(
        many=True,
        read_only=True)

    facilities_objs = PrisonFacilitySerializer(
        many=True,
        source='facilities',
        read_only=True)

    facilitylinks = PrisonFacilityLinkSerializer(
        many=True,
        read_only=True)

    opened_year = api.fields.GregorianYearField()
    opened_month = api.fields.GregorianMonthField()
    opened_day = api.fields.GregorianDayField()
    opened_year_fa = api.fields.FarsiYearField()
    opened_month_fa = api.fields.FarsiMonthField()
    opened_day_fa = api.fields.FarsiDayField()

    picture_resized = api.fields.ThumbnailImageField(source='picture')
    picture_200x200 = api.fields.ThumbnailImageField(source='picture', size=(200, 200))

    class Meta(PrisonSummarySerializer.Meta):
        fields = PrisonSummarySerializer.Meta.fields + (
            'address_en',
            'address_fa',
            'dean_name_en',
            'dean_name_fa',
            'dean_email',
            'dean_phone',
            'capacity',
            'capacity_is_estimate',
            'latitude',
            'longitude',
            'opened_year',
            'administered_by',
            'opened_month',
            'opened_day',
            'opened_year_fa',
            'opened_month_fa',
            'opened_day_fa',
            'physical_structure_en',
            'physical_structure_fa',
            'size_and_density_en',
            'size_and_density_fa',
            'medicine_and_nutrition_en',
            'medicine_and_nutrition_fa',
            'facilities_objs',
            'bio_en',
            'bio_fa',
            'quotes',
            'facilitylinks',
            'files',
            'timeline',
            'sources',
            'comments',
            'picture',
            'picture_resized',
            'picture_200x200',
            'explanation_en',
            'explanation_fa',
            'explanation_aea_en',
            'explanation_aea_fa',
        )
        writable_many_many_fields = (
            'facilities_objs',
        )
