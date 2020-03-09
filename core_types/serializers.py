
import django.db.models
import rest_framework.serializers

import api.fields
import api.serializers
import core_types.models


BASE_FIELDS = (
    'id',
    'url',
)


PUBLISHABLE_FIELDS = BASE_FIELDS + (
    'is_published',
    'created',
    'updated',
    'created_by',
    'updated_by',
)


PUBLISHABLE_READ_ONLY_FIELDS = (
    'created',
    'updated',
    'created_by',
    'updated_by',
)


class PublishableListSerializer(rest_framework.serializers.ListSerializer):
    """
    This ListSerializer automatically filters is_published=False models if the
    user isn't logged in. It should be set as the
    Serializer.meta.list_serializer_class for any serializer that handles a
    PublishableMixin model.

    See https://github.com/smallmedia/united/issues/84
    """
    def to_representation(self, value):
        user = getattr(self.context.get('request'), 'user', None)
        if not (user and user.is_authenticated()):
            if isinstance(value, (django.db.models.QuerySet,
                                  django.db.models.Manager)):
                value = value.all().filter(is_published=True)
            else:
                value = [v for v in value if v.is_published]
        return super(PublishableListSerializer, self).to_representation(value)


class PublishableModelSerializer(api.serializers.ModelSerializer):
    created_by = api.serializers.UserSerializer(read_only=True)
    updated_by = api.serializers.UserSerializer(read_only=True)

    def get_fields(self):
        """
        Override get_fields() to allow hiding created_by/updated_by if the user
        hasn't requested them. This cuts down on the number of SQL queries
        required to render the response.

        Request created_by/updated_by fields by including ?verbose=1 in the
        HTTP GET query string.
        """
        fields = super(PublishableModelSerializer, self).get_fields()
        request = self.context.get('request')

        if request and not request.GET.get('verbose'):
            fields.pop('created_by')
            fields.pop('updated_by')
            fields.pop('created')
            fields.pop('updated')
        return fields

    class Meta:
        fields = PUBLISHABLE_FIELDS
        read_only_fields = PUBLISHABLE_READ_ONLY_FIELDS
        list_serializer_class = PublishableListSerializer


class ChoiceSerializer(PublishableModelSerializer):
    class Meta(PublishableModelSerializer.Meta):
        fields = PublishableModelSerializer.Meta.fields + (
            'name_en',
            'name_fa',
        )


class QuoteSerializer(PublishableModelSerializer):
    class Meta(PublishableModelSerializer.Meta):
        fields = PublishableModelSerializer.Meta.fields + (
            'name_en',
            'name_fa',
            'quote_en',
            'quote_fa',
            'source',
        )


class FileSerializer(PublishableModelSerializer):
    file_thumb_resized = api.fields.ThumbnailImageField(source='file_thumb')

    class Meta(PublishableModelSerializer.Meta):
        fields = PublishableModelSerializer.Meta.fields + (
            'name_en',
            'name_fa',
            'description_en',
            'description_fa',
            'file',
            'file_thumb',
            'file_thumb_resized',
        )


class TimelineSerializer(PublishableModelSerializer):
    year = api.fields.GregorianYearField()
    month = api.fields.GregorianMonthField()
    day = api.fields.GregorianDayField()
    year_fa = api.fields.FarsiYearField()
    month_fa = api.fields.FarsiMonthField()
    day_fa = api.fields.FarsiDayField()

    class Meta(PublishableModelSerializer.Meta):
        fields = PublishableModelSerializer.Meta.fields + (
            'year',
            'month',
            'day',
            'year_fa',
            'month_fa',
            'day_fa',
            'timeline_is_estimate',
            'source_link',
            'description_en',
            'description_en_html',
            'description_fa',
            'description_fa_html',
        )


class SourceSerializer(api.serializers.ModelSerializer):
    class Meta(PublishableModelSerializer.Meta):
        fields = PublishableModelSerializer.Meta.fields + (
            'link',
            'name',
            'description',
            'related_fields'
        )

    def get_extra_kwargs(self):
        base = super(SourceSerializer, self).get_extra_kwargs()
        return dict(base, **{
            'related_fields': {
                'required': False,
            }
        })


class CommentSerializer(api.serializers.ModelSerializer):
    user = api.serializers.UserSerializer(required=False, read_only=True)

    class Meta:
        fields = BASE_FIELDS + (
            'user',
            'created',
            'comment',
        )


class ProvinceSerializer(ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:province-detail')

    class Meta(ChoiceSerializer.Meta):
        model = core_types.models.Province


class CitySerializer(ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:city-detail')

    province = ProvinceSerializer(read_only=True)

    class Meta(ChoiceSerializer.Meta):
        model = core_types.models.City
        fields = ChoiceSerializer.Meta.fields + (
            'province',
            'located_in_iran',
        )
        writable_nested_fields = (
            'province',
        )


class CountrySerializer(ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:country-detail')

    class Meta(ChoiceSerializer.Meta):
        model = core_types.models.Country


class EthnicitySerializer(ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:ethnicity-detail')

    class Meta(ChoiceSerializer.Meta):
        model = core_types.models.Ethnicity


class ReligionSerializer(ChoiceSerializer):
    url = rest_framework.serializers.HyperlinkedIdentityField(
        view_name='api:religion-detail')

    class Meta(ChoiceSerializer.Meta):
        model = core_types.models.Religion
