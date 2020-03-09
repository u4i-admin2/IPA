
import api.tests
import prisoners.models
import prisoners.viewsets


class ExtraArgsMixin(object):
    def get_mommy_extra_args(self):
        return {
            'prisoner': self.mommy.make(prisoners.models.Prisoner)
        }


class PrisonerQuoteViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerQuoteViewSet
    name_prefix = 'api:prisonerquote'


class PrisonerFileViewSetTest(ExtraArgsMixin,
                              api.tests.FileUploadViewSetMixin,
                              api.tests.ViewSetMixin,
                              api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerFileViewSet
    name_prefix = 'api:prisonerfile'


class PrisonerRelationshipViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerRelationshipViewSet
    name_prefix = 'api:prisonerrelationship'


class PrisonerAffiliationViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerAffiliationViewSet
    name_prefix = 'api:prisoneraffiliation'

    def get_mommy_extra_args(self):
        return {
            'prisoner': self.mommy.make(prisoners.models.Prisoner),
            'organisation': self.mommy.make(prisoners.models.Organisation)
        }


class PrisonerArrestViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerArrestViewSet
    name_prefix = 'api:prisonerarrest'


class PrisonerDetentionViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerDetentionViewSet
    name_prefix = 'api:prisonerdetention'


class PrisonerSentenceViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerSentenceViewSet
    name_prefix = 'api:prisonersentence'


class PrisonerTimelineViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerTimelineViewSet
    name_prefix = 'api:prisonertimeline'


class RelationshipTypeViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.RelationshipTypeViewSet
    name_prefix = 'api:relationshiptype'


class OrganisationViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.OrganisationViewSet
    name_prefix = 'api:organisation'


class ActivityPersecutedForViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.ActivityPersecutedForViewSet
    name_prefix = 'api:activitypersecutedfor'


class ChargedWithViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.ChargedWithViewSet
    name_prefix = 'api:chargedwith'


class CaseIdViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.CaseIdViewSet
    name_prefix = 'api:caseid'


class DomesticLawViolatedViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.DomesticLawViolatedViewSet
    name_prefix = 'api:domesticlawviolated'


class InternationalLawViolatedViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.InternationalLawViolatedViewSet
    name_prefix = 'api:internationallawviolated'


class DetentionStatusViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.DetentionStatusViewSet
    name_prefix = 'api:detentionstatus'


class PrisonTreatmentViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonTreatmentViewSet
    name_prefix = 'api:prisontreatment'


class PrisonerSourceViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerSourceViewSet
    name_prefix = 'api:prisonersource'


class PrisonerCommentViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerCommentViewSet
    name_prefix = 'api:prisonercomment'

    def get_mommy_extra_args(self):
        return {
            'user': self.user
        }


class SentenceBehaviourViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.SentenceBehaviourViewSet
    name_prefix = 'api:sentencebehaviour'


class PrisonerViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerViewSet
    name_prefix = 'api:prisoner'

    publishable_child_relation_name = 'quotes'

    def make_publishable_child_relation(self, mod):
        quote = prisoners.models.PrisonerQuote(prisoner_id=mod.pk, quote='test')
        quote.save()
        return quote


class PrisonerPictureViewSetTest(api.tests.ImageUploadViewSetMixin,
                                 api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerPictureViewSet
    name_prefix = 'api:prisonerpictures'


class PrisonerTaglistViewSetTest(api.tests.TaglistViewSetMixin,
                                 api.tests.TestCase):
    viewset_class = prisoners.viewsets.PrisonerTagListViewSet
    name_prefix = 'api:prisonertaglist'
