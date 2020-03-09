
import api.viewsets
import core_types.models
import core_types.serializers


class CityViewSet(api.viewsets.ChoiceViewSet):
    queryset = (core_types.models.City.objects.all().prefetch_related('province'))
    serializer_class = core_types.serializers.CitySerializer
    # search_fields = api.viewsets.ChoiceViewSet.search_fields + (
    #     'province__name_en',
    #     'province__name_fa',
    # )


class CountryViewSet(api.viewsets.ChoiceViewSet):
    queryset = core_types.models.Country.objects.all()
    serializer_class = core_types.serializers.CountrySerializer


class EthnicityViewSet(api.viewsets.ChoiceViewSet):
    queryset = core_types.models.Ethnicity.objects.all()
    serializer_class = core_types.serializers.EthnicitySerializer


class ProvinceViewSet(api.viewsets.ChoiceViewSet):
    queryset = core_types.models.Province.objects.all()
    serializer_class = core_types.serializers.ProvinceSerializer


class ReligionViewSet(api.viewsets.ChoiceViewSet):
    queryset = core_types.models.Religion.objects.all()
    serializer_class = core_types.serializers.ReligionSerializer


VIEWSETS = [
    CityViewSet,
    CountryViewSet,
    EthnicityViewSet,
    ProvinceViewSet,
    ReligionViewSet,
]
