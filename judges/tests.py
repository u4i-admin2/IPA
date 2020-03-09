
import api.tests
import judges.viewsets


class ExtraArgsMixin(object):
    def get_mommy_extra_args(self):
        return {
            'judge': self.mommy.make(judges.models.Judge)
        }


class SentenceTypeViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = judges.viewsets.SentenceTypeViewSet
    name_prefix = 'api:sentencetype'


class BehaviourTypeViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = judges.viewsets.BehaviourTypeViewSet
    name_prefix = 'api:behaviourtype'


class CourtAndBranchViewSetTest(api.tests.ChoiceViewSetMixin, api.tests.TestCase):
    viewset_class = judges.viewsets.CourtAndBranchViewSet
    name_prefix = 'api:courtandbranch'


class JudgeTimelineViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = judges.viewsets.JudgeTimelineViewSet
    name_prefix = 'api:judgetimeline'


class JudgePositionViewSetTest(api.tests.ViewSetMixin,
                               api.tests.TestCase):
    viewset_class = judges.viewsets.JudgePositionViewSet
    name_prefix = 'api:judgeposition'

    def get_mommy_extra_args(self):
        return {
            'judge': self.mommy.make(judges.models.Judge),
            'court_and_branch': self.mommy.make(judges.models.CourtAndBranch),
            'judicial_position': self.mommy.make(judges.models.JudicialPosition),
        }


class JudgeSourceViewSetTest(ExtraArgsMixin,
                             api.tests.ViewSetMixin,
                             api.tests.TestCase):
    viewset_class = judges.viewsets.JudgeSourceViewSet
    name_prefix = 'api:judgesource'


class JudgeQuoteViewSetTest(ExtraArgsMixin,
                            api.tests.ViewSetMixin,
                            api.tests.TestCase):
    viewset_class = judges.viewsets.JudgeQuoteViewSet
    name_prefix = 'api:judgequote'


class JudgeFileViewSetTest(ExtraArgsMixin,
                           api.tests.FileUploadViewSetMixin,
                           api.tests.ViewSetMixin,
                           api.tests.TestCase):
    viewset_class = judges.viewsets.JudgeFileViewSet
    name_prefix = 'api:judgefile'


class JudgeCommentViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = judges.viewsets.JudgeCommentViewSet
    name_prefix = 'api:judgecomment'

    def get_mommy_extra_args(self):
        return {
            'user': self.user
        }


class JudgeViewSetTest(api.tests.ViewSetMixin, api.tests.TestCase):
    viewset_class = judges.viewsets.JudgeViewSet
    name_prefix = 'api:judge'

    publishable_child_relation_name = 'quotes'

    def make_publishable_child_relation(self, mod):
        quote = judges.models.JudgeQuote(judge_id=mod.pk, quote='test')
        quote .save()
        return quote


class JudgePictureViewSetTest(api.tests.ImageUploadViewSetMixin,
                              api.tests.TestCase):
    viewset_class = judges.viewsets.JudgePictureViewSet
    name_prefix = 'api:judgepictures'


class JudgeTaglistViewSetTest(api.tests.TaglistViewSetMixin,
                              api.tests.TestCase):
    viewset_class = judges.viewsets.JudgeTagListViewSet
    name_prefix = 'api:judgetaglist'
