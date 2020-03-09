
import api.tests
import prisons.models
import prisons.viewsets


class ExtraArgsMixin(object):
    def get_mommy_extra_args(self):
        return {
            'prison': self.mommy.make(prisons.models.Prison)
        }


class PrisonQuoteViewSetMixin(ExtraArgsMixin, api.tests.ViewSetMixin,
                              api.tests.TestCase):
    viewset_class = prisons.viewsets.PrisonQuoteViewSet
    name_prefix = 'api:prisonquote'


class PrisonFileViewSetMixin(ExtraArgsMixin,
                             api.tests.FileUploadViewSetMixin,
                             api.tests.ViewSetMixin,
                             api.tests.TestCase):
    viewset_class = prisons.viewsets.PrisonFileViewSet
    name_prefix = 'api:prisonfile'


class PrisonTimelineViewSetMixin(ExtraArgsMixin, api.tests.ViewSetMixin,
                                 api.tests.TestCase):
    viewset_class = prisons.viewsets.PrisonTimelineViewSet
    name_prefix = 'api:prisontimeline'


class PrisonFacilityViewSetMixin(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisons.viewsets.PrisonFacilityViewSet
    name_prefix = 'api:prisonfacility'


class PrisonSourceViewSetMixin(ExtraArgsMixin, api.tests.ViewSetMixin,
                               api.tests.TestCase):
    viewset_class = prisons.viewsets.PrisonSourceViewSet
    name_prefix = 'api:prisonsource'


class PrisonCommentViewSetMixin(ExtraArgsMixin, api.tests.ViewSetMixin,
                                api.tests.TestCase):
    viewset_class = prisons.viewsets.PrisonCommentViewSet
    name_prefix = 'api:prisoncomment'

    def get_mommy_extra_args(self):
        return {
            'user': self.user
        }


class PrisonViewSetMixin(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisons.viewsets.PrisonViewSet
    name_prefix = 'api:prison'

    publishable_child_relation_name = 'quotes'

    def make_publishable_child_relation(self, mod):
        quote = prisons.models.PrisonQuote(prison_id=mod.pk, quote='test')
        quote.save()
        return quote


class PrisonTaglistViewSetTest(api.tests.TaglistViewSetMixin,
                               api.tests.TestCase):
    viewset_class = prisons.viewsets.PrisonTagListViewSet
    name_prefix = 'api:prisontaglist'
