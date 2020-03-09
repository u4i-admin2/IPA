import json
import django.test
from django.core.urlresolvers import reverse_lazy

import public.test_fixtures
import prisons.models
import prisoners.models
import judges.models


class RendersTemplateMixin(object):
    def test_template_renders(self):
        resp = self.client.get(self.url)
        self.assertEquals(200, resp.status_code)


class PrisonViewTest(RendersTemplateMixin, django.test.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        PrisonerA has 2 arrest instances and 3 detention instances
        Prisoner B has 2 arrest instance and 2 detention instance

        We're asserting that we get the latest arrest and then the lastest detention, in this case

        PrisonerA has 2 arrest instances and 3 detention instances -> prisoner > arrestA2 > detentionA2 (PrisonA)
        PrisonerB has 2 arrest instances and 2 detention instances -> prisoner > arrestB1 > detentionB1 (Prison A)

        """
        super(PrisonViewTest, cls).setUpClass()
        public.test_fixtures.fixtures_for_prison_view(cls)

    @classmethod
    def tearDownClass(cls):
        public.test_fixtures.generic_teardown()

    @property
    def url(self):
        return reverse_lazy('public:prison', kwargs={'pk': self.prison.pk})

    def test_mistreatments(self):
        resp = self.client.get(self.url)
        resp.data = json.loads(resp.data['data'])
        assert resp.data['political_prisoners'] == 2
        assert resp.data['stats']['top_judge'] == [[u'JudgeA', 1]]
        assert resp.data['stats']['top_religion'] == [[u'wobbles', 1]]
        assert resp.data['stats']['top_ethnicity'] == [[u'bobbles', 1]]
        assert resp.data['stats']['top_charges'] == [[u'Charge B', 2], [u'Charge C', 1]]
        assert resp.data['stats']['top_mistreatment'] == [u'Treatment A', 2]

        assert resp.data['stats']['total_charges'] == 3
        print 'mis', resp.data['stats']['total_mistreatments']
        self.assertEqual(resp.data['stats']['total_mistreatments'], 4)

        # {u'Treatment C': [2], u'Treatment B': [1], u'Treatment A': [2, 1]}
        id_a = self.prisonerA.id
        id_b = self.prisonerB.id
        assert resp.data['mistreatments']['Treatment C'] == [id_b]
        assert resp.data['mistreatments']['Treatment B'] == [id_a]
        assert resp.data['mistreatments']['Treatment A'] == [id_b, id_a]

    def test_unpublished_404s(self):
        url = reverse_lazy('public:prison', kwargs={'pk': self.prisonC.pk})
        resp = self.client.get(url)
        self.assertEquals(404, resp.status_code)


class JudgeViewTest(RendersTemplateMixin, django.test.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        prisA -> arrestA1 (chargeC, activityA,B) -> sentenceA, sentenceB (behaviour A, behaviour B)
        prisB -> arrestB1, B2 (chargeA,B/B, activity C/B) -> sentenceB, sentenceB2, sentenceB3 (C, A, A)
        """
        super(JudgeViewTest, cls).setUpClass()
        public.test_fixtures.fixtures_for_judge_view(cls)

    @classmethod
    def tearDownClass(cls):
        public.test_fixtures.generic_teardown()

    @property
    def url(self):
        return reverse_lazy('public:judge', kwargs={'pk': self.judge.pk})

    def test_violations(self):
        resp = self.client.get(self.url)
        resp.data = json.loads(resp.data['data'])
        assert resp.data['total_sentences'] == 5
        assert resp.data['total_time_sentenced'] == 54.8
        self.assertEqual(resp.data['average_sentence'], 10.9)
        id_a = self.prisonerA.id
        id_b = self.prisonerB.id
        assert id_a in resp.data['behaviours']['Behaviour A']
        assert id_b in resp.data['behaviours']['Behaviour A']
        assert id_a in resp.data['behaviours']['Behaviour B']
        assert id_b not in resp.data['behaviours']['Behaviour B']
        assert id_a not in resp.data['behaviours']['Behaviour C']
        assert id_b in resp.data['behaviours']['Behaviour C']
        assert resp.data['stats']['top_behaviour'] == [u'Behaviour A', 3]
        assert resp.data['stats']['total_behaviours'] == 6
        assert resp.data['stats']['total_charges'] == 6
        assert resp.data['stats']['top_charges'] == [[u'Charge B', 3], [u'Charge A', 2]]
        assert resp.data['stats']['total_activities'] == 4
        self.assertEqual(resp.data['stats']['top_activity'], [[u'Unknown', 4]])
        assert resp.data['stats']['top_ethnicity'] == [[u'ethnicityA', 5]]
        assert resp.data['stats']['top_religion'] == [[u'religionA', 5]]

    def test_unpublished_404s(self):
        url = reverse_lazy('public:judge', kwargs={'pk': self.judgeUnpublished.pk})
        resp = self.client.get(url)
        self.assertEquals(404, resp.status_code)


class PrisonersViewTest(RendersTemplateMixin, django.test.TestCase):

    @classmethod
    def setUpClass(cls):
        public.test_fixtures.fixtures_for_prison_view(cls)

    @classmethod
    def tearDownClass(cls):
        public.test_fixtures.generic_teardown()

    @property
    def url(self):
        return reverse_lazy('public:prisoners')

    def all_in(self, candidates, sequence):
        for element in candidates:
            if element not in sequence:
                return False
        return True

    def test_prisoners(self):
        resp = self.client.get(self.url)
        dimensions = json.loads(resp.context_data['dimensions'])
        pris_lookup = json.loads(resp.context_data['chart_entity_hover_info'])

        pris_a = prisoners.models.Prisoner.objects.get(surname='flob').id  # 11
        pris_b = prisoners.models.Prisoner.objects.get(surname='blob').id  # 12
        pris_d = prisoners.models.Prisoner.objects.get(surname='Mr D').id  # 13
        pris_e = prisoners.models.Prisoner.objects.get(surname='Mr E').id  # 14
        pris_f = prisoners.models.Prisoner.objects.get(surname='Mr F').id  # 15

        assert len(pris_lookup.keys()) == 5
        # religion
        assert self.all_in([pris_a, pris_e], dimensions['religion']['wobbles'])
        assert self.all_in([pris_f, pris_d], dimensions['religion']['nibbles'])
        assert pris_b in dimensions['religion']['Unknown']
        # charges
        assert self.all_in([pris_a, pris_b, pris_d, pris_e], dimensions['charges']['Charge A'])
        assert self.all_in([pris_f, pris_e], dimensions['charges']['Charge B'])
        assert self.all_in([pris_d, pris_f], dimensions['charges']['Charge C'])
        # ethnicities
        assert self.all_in([pris_d, pris_e], dimensions['ethnicity']['nobbles'])
        assert self.all_in([pris_b, pris_f], dimensions['ethnicity']['bobbles'])
        assert self.all_in([pris_a], dimensions['ethnicity']['Unknown'])
        # activities
        assert self.all_in([pris_a, pris_b], dimensions['activity']['Activity A'])
        assert self.all_in([pris_f], dimensions['activity']['Activity C'])
        # sentence (none)
        # {u'charges': {u'Charge A': [11, 12, 14, 15], u'Charge B': [15, 16], u'Charge C': [14, 16]}
        assert self.all_in([pris_a, pris_b, pris_d, pris_e], dimensions['charges']['Charge A'])
        assert self.all_in([pris_e, pris_f], dimensions['charges']['Charge B'])
        assert self.all_in([pris_d, pris_f], dimensions['charges']['Charge C'])
        # treatments
        assert self.all_in([pris_d, pris_e], dimensions['mistreatments']['Treatment A'])
        assert self.all_in([pris_d, pris_f], dimensions['mistreatments']['Treatment B'])
        assert self.all_in([pris_a, pris_e, pris_f], dimensions['mistreatments']['Treatment C'])


class JudgesViewTest(django.test.TestCase):
    # RendersTemplateMixin,
    @classmethod
    def setUpClass(cls):
        public.test_fixtures.fixtures_for_judge_view(cls)

    @classmethod
    def tearDownClass(cls):
        public.test_fixtures.generic_teardown()

    @property
    def url(self):
        return reverse_lazy('public:judges')

    def test_judges(self):
        resp = self.client.get(self.url)
        data = json.loads(resp.context_data['judges'])

        judge_a = judges.models.Judge.objects.get(surname='JudgeA').id
        # judge_b = judges.models.Judge.objects.get(surname='JudgeB').id
        judge_c = judges.models.Judge.objects.get(surname='JudgeC').id

        assert len(data.keys()) == 3
        # judge a
        assert data[str(judge_a)]['stats']['prisoners_sentenced'] == 2
        assert data[str(judge_a)]['stats']['total_verdicts'] == 5
        assert data[str(judge_a)]['stats']['total_months'] == 33
        assert data[str(judge_a)]['stats']['total_years'] == 52
        assert data[str(judge_a)]['stats']['total_lashes'] == 200
        assert data[str(judge_a)]['stats']['total_executions'] == 2
        assert data[str(judge_a)]['stats']['total_mistreatments'] == 2
        # judge c
        assert data[str(judge_c)]['stats']['prisoners_sentenced'] == 1
        assert data[str(judge_c)]['stats']['total_verdicts'] == 1
        assert data[str(judge_c)]['stats']['total_months'] == 10
        assert data[str(judge_c)]['stats']['total_years'] == 8
        assert data[str(judge_c)]['stats']['total_lashes'] == 27
        assert data[str(judge_c)]['stats']['total_executions'] == 1
        assert data[str(judge_c)]['stats']['total_mistreatments'] == 1


class PrisonsViewTest(RendersTemplateMixin, django.test.TestCase):

    @classmethod
    def setUpClass(cls):
        super(PrisonsViewTest, cls).setUpClass()
        public.test_fixtures.fixtures_for_prison_view(cls)

    @classmethod
    def tearDownClass(cls):
        public.test_fixtures.generic_teardown()

    @property
    def url(self):
        return reverse_lazy('public:prisons')

    def test_prisons(self):
        resp = self.client.get(self.url)
        data = json.loads(resp.context_data['prisons'])

        prison_a = prisons.models.Prison.objects.get(name='PrisonA').id
        prison_b = prisons.models.Prison.objects.get(name='PrisonB').id
        prison_d = prisons.models.Prison.objects.get(name='PrisonD').id

        assert len(data.keys()) == 3
        assert data[str(prison_a)]['total_prisoners'] == 2
        assert data[str(prison_b)]['total_prisoners'] == 1
        assert data[str(prison_d)]['total_prisoners'] == 2
        # genders
        assert data[str(prison_a)]['genders'] == {u'M': 1, u'F': 1}
        assert data[str(prison_b)]['genders'] == {u'M': 1, u'F': 0}
        assert data[str(prison_d)]['genders'] == {u'M': 1, u'F': 1}
        # religion
        self.assertEqual(data[str(prison_a)]['religions'], {u'wobbles': 1, u'nibbles': 0, u'Unknown': 1})
        assert data[str(prison_b)]['religions'] == {u'wobbles': 0, u'nibbles': 1, u'Unknown': 0}
        assert data[str(prison_d)]['religions'] == {u'wobbles': 1, u'nibbles': 1, u'Unknown': 0}
        # ethnicity
        assert data[str(prison_a)]['ethnicities'] == {u'nobbles': 0, u'Unknown': 1, u'bobbles': 1}
        assert data[str(prison_b)]['ethnicities'] == {u'nobbles': 0, u'Unknown': 0, u'bobbles': 1}
        assert data[str(prison_d)]['ethnicities'] == {u'nobbles': 2, u'Unknown': 0, u'bobbles': 0}
        # charges
        assert data[str(prison_a)]['charges'] == {u'Charge A': 0, u'Charge B': 2, u'Charge C': 1}
        assert data[str(prison_b)]['charges'] == {u'Charge A': 0, u'Charge B': 1, u'Charge C': 1}
        assert data[str(prison_d)]['charges'] == {u'Charge A': 2, u'Charge B': 1, u'Charge C': 1}
        # mistreatments
        assert data[str(prison_a)]['treatments'] == {u'Treatment C': 1, u'Treatment B': 1, u'Treatment A': 2}
        assert data[str(prison_b)]['treatments'] == {u'Treatment C': 1, u'Treatment B': 1, u'Treatment A': 0}
        assert data[str(prison_d)]['treatments'] == {u'Treatment C': 1, u'Treatment B': 1, u'Treatment A': 2}
        # activities
        assert data[str(prison_a)]['activities'] == {u'Activity A': 2, u'Activity C': 0, u'Activity B': 0}
        assert data[str(prison_b)]['activities'] == {u'Activity A': 0, u'Activity C': 1, u'Activity B': 0}
        assert data[str(prison_d)]['activities'] == {u'Unknown': 2, u'Activity A': 0, u'Activity C': 0, u'Activity B': 0}
