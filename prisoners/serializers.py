

import rest_framework.serializers

import api.fields
import core_types.models
import core_types.serializers
import prisoners.models
import prisons.serializers
import judges.serializers


class PrisonerQuoteSerializer(core_types.serializers.QuoteSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonerquote-detail')
    prisoner_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.QuoteSerializer.Meta):
        model = prisoners.models.PrisonerQuote
        fields = core_types.serializers.QuoteSerializer.Meta.fields + (
            'prisoner_id',
        )


class PrisonerFileSerializer(core_types.serializers.FileSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonerfile-detail')
    prisoner_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.FileSerializer.Meta):
        model = prisoners.models.PrisonerFile
        fields = core_types.serializers.FileSerializer.Meta.fields + (
            'prisoner_id',
            'file_type',
        )


class PrisonerTimelineSerializer(core_types.serializers.TimelineSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonertimeline-detail')
    prisoner_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.TimelineSerializer.Meta):
        model = prisoners.models.PrisonerTimeline
        fields = core_types.serializers.TimelineSerializer.Meta.fields + (
            'prisoner_id',
        )


class RelationshipTypeSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:relationshiptype-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisoners.models.RelationshipType


class OrganisationSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:organisation-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisoners.models.Organisation


class PrisonerAffiliationSerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisoneraffiliation-detail')
    prisoner_id = rest_framework.serializers.IntegerField()

    organisation = OrganisationSerializer(
        read_only=True)

    relationship_type = RelationshipTypeSerializer(
        read_only=True)

    # confirmed = rest_framework.serializers.BooleanField(
    #     read_only=True)

    class Meta(core_types.serializers.PublishableModelSerializer.Meta):
        model = prisoners.models.PrisonerAffiliation
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'prisoner_id',
            'organisation',
            'relationship_type',
            'confirmed',
        )
        writable_nested_fields = (
            'organisation',
            'relationship_type',
            # 'confirmed',
        )


class ActivityPersecutedForSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:activitypersecutedfor-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisoners.models.ActivityPersecutedFor


class ChargedWithSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:chargedwith-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisoners.models.ChargedWith


class CaseIdSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:caseid-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisoners.models.CaseId


class DomesticLawViolatedSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:domesticlawviolated-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisoners.models.DomesticLawViolated


class InternationalLawViolatedSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:internationallawviolated-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisoners.models.InternationalLawViolated


class DetentionStatusSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:detentionstatus-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisoners.models.DetentionStatus
        fields = core_types.serializers.ChoiceSerializer.Meta.fields + (
            'detained',
        )


class PrisonTreatmentSerializer(core_types.serializers.ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisontreatment-detail')

    class Meta(core_types.serializers.ChoiceSerializer.Meta):
        model = prisoners.models.PrisonTreatment


class PrisonerSourceSerializer(core_types.serializers.SourceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonersource-detail')
    prisoner_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.SourceSerializer.Meta):
        model = prisoners.models.PrisonerSource
        fields = core_types.serializers.SourceSerializer.Meta.fields + (
            'prisoner_id',
        )


class PrisonerCommentSerializer(core_types.serializers.CommentSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonercomment-detail')
    prisoner_id = rest_framework.serializers.IntegerField()

    class Meta(core_types.serializers.CommentSerializer.Meta):
        model = prisoners.models.PrisonerComment
        fields = core_types.serializers.CommentSerializer.Meta.fields + (
            'prisoner_id',
        )


class PrisonerDetentionSerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonerdetention-detail')
    arrest_id = rest_framework.serializers.IntegerField()

    prison = prisons.serializers.PrisonSummarySerializer(
        allow_null=True,
        read_only=True)

    treatment_objs = PrisonTreatmentSerializer(
        many=True,
        source='treatment',
        read_only=True)

    detention_year = api.fields.GregorianYearField()
    detention_month = api.fields.GregorianMonthField()
    detention_day = api.fields.GregorianDayField()
    detention_year_fa = api.fields.FarsiYearField()
    detention_month_fa = api.fields.FarsiMonthField()
    detention_day_fa = api.fields.FarsiDayField()

    class Meta:
        model = prisoners.models.PrisonerDetention
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'arrest_id',
            'prison',
            'detention_type',
            'treatment_objs',
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
        writable_many_many_fields = (
            'treatment_objs',
        )


class SentenceBehaviourSerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:sentencebehaviour-detail')
    sentence_id = rest_framework.serializers.IntegerField()

    behaviour_type = judges.serializers.BehaviourTypeSerializer(
        read_only=True)

    class Meta:
        model = prisoners.models.SentenceBehaviour
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'sentence_id',
            'behaviour_type',
            'description_en',
            'description_fa',
        )
        writable_nested_fields = (
            'behaviour_type',
        )


class PrisonerSentenceSerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonersentence-detail')
    arrest_id = rest_framework.serializers.IntegerField()

    judge = judges.serializers.JudgeSummarySerializer(
        allow_null=True,
        read_only=True)

    court_and_branch = judges.serializers.CourtAndBranchSerializer(
        allow_null=True,
        read_only=True)

    behaviours = SentenceBehaviourSerializer(
        many=True,
        read_only=True)

    sentence_type_objs = judges.serializers.SentenceTypeSerializer(
        many=True,
        source='sentence_type',
        read_only=True)

    class Meta:
        model = prisoners.models.PrisonerSentence
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'arrest_id',
            'judge',
            'court_and_branch',
            'behaviours',
            'death_penalty',
            'exiled',
            'life',
            'social_depravation_en',
            'social_depravation_fa',
            'fine',
            'number_of_lashes',
            'sentence_months',
            'sentence_years',
            'sentence_type_objs',
        )
        writable_nested_fields = (
            'judge',
            'court_and_branch',
        )
        writable_many_many_fields = (
            'sentence_type_objs',
        )


class PrisonerArrestSerializer(core_types.serializers.PublishableModelSerializer):

    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonerarrest-detail')
    prisoner_id = rest_framework.serializers.IntegerField()

    case_id = CaseIdSerializer(
        allow_null=True,
        read_only=True)

    city = core_types.serializers.CitySerializer(
        allow_null=True,
        read_only=True)

    province = core_types.serializers.ProvinceSerializer(
        allow_null=True,
        read_only=True)

    activity_persecuted_for = ActivityPersecutedForSerializer(
        allow_null=True,
        read_only=True)

    secondary_activity = ActivityPersecutedForSerializer(
        allow_null=True,
        read_only=True)

    tertiary_activity = ActivityPersecutedForSerializer(
        allow_null=True,
        read_only=True)

    charged_with_objs = ChargedWithSerializer(
        many=True,
        source='charged_with',
        read_only=True)

    domestic_law_violated_objs = DomesticLawViolatedSerializer(
        many=True,
        source='domestic_law_violated',
        read_only=True)

    international_law_violated_objs = InternationalLawViolatedSerializer(
        many=True,
        source='international_law_violated',
        read_only=True)

    sentences = PrisonerSentenceSerializer(
        many=True,
        read_only=True)

    detentions = PrisonerDetentionSerializer(
        many=True,
        read_only=True)

    arrest_year = api.fields.GregorianYearField()
    arrest_month = api.fields.GregorianMonthField()
    arrest_day = api.fields.GregorianDayField()
    arrest_year_fa = api.fields.FarsiYearField()
    arrest_month_fa = api.fields.FarsiMonthField()
    arrest_day_fa = api.fields.FarsiDayField()

    class Meta:
        model = prisoners.models.PrisonerArrest
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'prisoner_id',
            'arrest_year',
            'arrest_month',
            'arrest_day',
            'arrest_year_fa',
            'arrest_month_fa',
            'arrest_day_fa',
            'activity_persecuted_for',
            'secondary_activity',
            'tertiary_activity',
            'case_id',
            'city',
            'province',
            'charged_with_objs',
            'domestic_law_violated_objs',
            'international_law_violated_objs',
            'sentences',
            'detentions',
        )
        writable_nested_fields = (
            'activity_persecuted_for',
            'secondary_activity',
            'tertiary_activity',
            'case_id',
            'city',
            'province',
        )
        writable_many_many_fields = (
            'charged_with_objs',
            'domestic_law_violated_objs',
            'international_law_violated_objs',
        )


class PrisonerSummarySerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisoner-detail')

    class Meta:
        model = prisoners.models.Prisoner
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'forename_en',
            'forename_fa',
            'surname_en',
            'surname_fa',
            'latest_activity_persecuted_for_name_en',
            'latest_activity_persecuted_for_name_fa',
            'latest_secondary_activity_name_en',
            'latest_secondary_activity_name_fa',
            'latest_tertiary_activity_name_en',
            'latest_tertiary_activity_name_fa',
            'latest_detention_status_name_en',
            'latest_prison_name_en',
            'latest_sentenced_judge_name_en',
            'latest_sentenced_judge_name_fa',
        )


class PrisonerRelationshipSerializer(core_types.serializers.PublishableModelSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:prisonerrelationship-detail')
    prisoner_id = rest_framework.serializers.IntegerField()

    relationship_type = RelationshipTypeSerializer(
        read_only=True)
    related_prisoner = PrisonerSummarySerializer(
        allow_null=True,
        read_only=True)

    class Meta:
        model = prisoners.models.PrisonerRelationship
        fields = core_types.serializers.PUBLISHABLE_FIELDS + (
            'prisoner_id',
            'forename_en',
            'forename_fa',
            'surname_en',
            'surname_fa',
            'relationship_type',
            'related_prisoner',
            'is_confirmed',
        )
        writable_nested_fields = (
            'relationship_type',
            'related_prisoner',
        )


class PrisonerSerializer(PrisonerSummarySerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(PrisonerSerializer, self).__init__(*args, **kwargs)

        if fields:
            excluded = set(fields)
            for field_name in excluded:
                try:
                    self.fields.pop(field_name)
                except KeyError:
                    pass

    religion = core_types.serializers.ReligionSerializer(
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

    detention_status = DetentionStatusSerializer(
        allow_null=True,
        read_only=True)

    quotes = PrisonerQuoteSerializer(
        many=True,
        read_only=True)

    files = PrisonerFileSerializer(
        many=True,
        read_only=True)

    sources = PrisonerSourceSerializer(
        many=True,
        read_only=True)

    comments = PrisonerCommentSerializer(
        many=True,
        read_only=True)

    affiliations = PrisonerAffiliationSerializer(
        many=True,
        read_only=True)

    relationships = PrisonerRelationshipSerializer(
        many=True,
        read_only=True)

    arrests = PrisonerArrestSerializer(
        many=True,
        read_only=True)

    timeline = PrisonerTimelineSerializer(
        many=True,
        read_only=True)

    home_countries_objs = core_types.serializers.CountrySerializer(
        many=True,
        source='home_countries',
        read_only=True)

    picture_resized = api.fields.ThumbnailImageField(source='picture')
    picture_200x200 = api.fields.ThumbnailImageField(source='picture', size=(200, 200))
    picture_30x30 = api.fields.ThumbnailImageField(source='picture', size=(30, 30))

    dob_year = api.fields.GregorianYearField()
    dob_month = api.fields.GregorianMonthField()
    dob_day = api.fields.GregorianDayField()
    dob_year_fa = api.fields.FarsiYearField()
    dob_month_fa = api.fields.FarsiMonthField()
    dob_day_fa = api.fields.FarsiDayField()

    detention_year = api.fields.GregorianYearField()
    detention_month = api.fields.GregorianMonthField()
    detention_day = api.fields.GregorianDayField()
    detention_year_fa = api.fields.FarsiYearField()
    detention_month_fa = api.fields.FarsiMonthField()
    detention_day_fa = api.fields.FarsiDayField()

    class Meta:
        model = prisoners.models.Prisoner
        fields = PrisonerSummarySerializer.Meta.fields + (
            'gender',
            'dob_year',
            'dob_month',
            'dob_day',
            'dob_year_fa',
            'dob_month_fa',
            'dob_day_fa',
            'religion',
            'birth_city',
            'birth_province',
            'ethnicity',
            'biography_en',
            'biography_fa',
            'picture',
            'picture_resized',
            'picture_200x200',
            'picture_30x30',
            'needs_attention',
            'quotes',
            'files',
            'sources',
            'comments',
            'affiliations',
            'relationships',
            'arrests',
            'home_countries_objs',
            'detention_status',
            'timeline',
            'detention_year',
            'detention_month',
            'detention_day',
            'detention_year_fa',
            'detention_month_fa',
            'detention_day_fa',
            'detention_is_approx',
            'explanation_en',
            'explanation_fa',
            'featured',
        )
        writable_nested_fields = (
            'religion',
            'birth_city',
            'birth_province',
            'ethnicity',
            'detention_status',
        )
        writable_many_many_fields = (
            'home_countries_objs',
        )
