
import api.tests
import core_types.models
import core_types.viewsets


class CityViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = core_types.viewsets.CityViewSet
    name_prefix = 'api:city'

    def get_mommy_extra_args(self):
        return {
            'province': self.mommy.make(core_types.models.Province)
        }


class CountryViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = core_types.viewsets.CountryViewSet
    name_prefix = 'api:country'


class EthnicityViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = core_types.viewsets.EthnicityViewSet
    name_prefix = 'api:ethnicity'


class ProvinceViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = core_types.viewsets.ProvinceViewSet
    name_prefix = 'api:province'


class ReligionViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = core_types.viewsets.ReligionViewSet
    name_prefix = 'api:religion'
