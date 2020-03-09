from rest_framework import serializers

from core_types.serializers import PublishableModelSerializer, PUBLISHABLE_FIELDS
from .models import FeaturedNews


class FeaturedNewsSerializer(PublishableModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:featurednews-detail')

    class Meta:
        model = FeaturedNews
        fields = PUBLISHABLE_FIELDS + (
            'language',
            'photo',
            'title',
            'excerpt',
            'link',
            'photo',
            'featured'
        )
