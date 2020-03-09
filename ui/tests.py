
import django.test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

import judges.models
import prisons.models
import prisoners.models


#
# Helpers.
#

class RequiresAuthMixin(object):
    login_url = reverse_lazy('ui:users:login')

    def test_requires_auth(self):
        resp = self.client.get(self.url)
        self.assertEquals(302, resp.status_code)
        self.assertTrue(str(self.login_url) in resp.url)

        User.objects.create_user('abcom', password='123')
        self.client.login(username='abcom', password='123')

        resp = self.client.get(self.url)
        self.assertEquals(200, resp.status_code)


class RendersTemplateMixin(object):
    def test_template_renders(self):
        User.objects.create_user('abcom', password='123')
        self.client.login(username='abcom', password='123')

        resp = self.client.get(self.url)
        self.assertEquals(200, resp.status_code)


#
# Dashboard.
#

class DashboardHomeViewTest(RequiresAuthMixin, RendersTemplateMixin,
                            django.test.TestCase):
    url = reverse_lazy('ui:dashboard:home')


class DashboardSearchResultsViewTest(RequiresAuthMixin, RendersTemplateMixin,
                                     django.test.TestCase):
    url = reverse_lazy('ui:dashboard:search_results')


class JudgeListViewTest(RequiresAuthMixin, RendersTemplateMixin,
                        django.test.TestCase):
    url = reverse_lazy('ui:dashboard:judge_list')


class NewJudgeViewTest(RequiresAuthMixin, RendersTemplateMixin,
                       django.test.TestCase):
    url = reverse_lazy('ui:dashboard:new_judge')


class JudgeDetailViewTest(RequiresAuthMixin, RendersTemplateMixin,
                          django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super(JudgeDetailViewTest, cls).setUpClass()
        cls.judge = judges.models.Judge.objects.create(
            forename='test',
            surname='judge')

    @property
    def url(self):
        return reverse_lazy('ui:dashboard:judge_detail',
                            kwargs={'pk': self.judge.pk})


class PrisonListViewTest(RequiresAuthMixin, RendersTemplateMixin,
                         django.test.TestCase):
    url = reverse_lazy('ui:dashboard:prison_list')


class NewPrisonViewTest(RequiresAuthMixin, RendersTemplateMixin,
                        django.test.TestCase):
    url = reverse_lazy('ui:dashboard:new_prison')


class PrisonDetailViewTest(RequiresAuthMixin, RendersTemplateMixin,
                           django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super(PrisonDetailViewTest, cls).setUpClass()
        cls.prison = prisons.models.Prison.objects.create(
            name='prison',
            address='prison',
            dean_name='prison',
            dean_email='prison',
            dean_phone='prison')

    @property
    def url(self):
        return reverse_lazy('ui:dashboard:prison_detail',
                            kwargs={'pk': self.prison.pk})


class PrisonerListViewTest(RequiresAuthMixin, RendersTemplateMixin,
                           django.test.TestCase):
    url = reverse_lazy('ui:dashboard:prisoner_list')


class NewPrisonerViewTest(RequiresAuthMixin, RendersTemplateMixin,
                          django.test.TestCase):
    url = reverse_lazy('ui:dashboard:new_prisoner')


class PrisonerDetailViewTest(RequiresAuthMixin, RendersTemplateMixin,
                             django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super(PrisonerDetailViewTest, cls).setUpClass()
        cls.prisoner = prisoners.models.Prisoner.objects.create(
            surname='surname')

    @property
    def url(self):
        return reverse_lazy('ui:dashboard:prisoner_detail',
                            kwargs={'pk': self.prisoner.pk})


#
# django.contrib.auth. We don't re-test contrib.auth logic here, simply ensure
# the templates render.
#

class LoginViewTest(RendersTemplateMixin, django.test.TestCase):
    url = reverse_lazy('ui:users:login')


class LogoutViewTest(RendersTemplateMixin, django.test.TestCase):
    url = reverse_lazy('ui:users:logout')


class PasswordChangeViewTest(RequiresAuthMixin, RendersTemplateMixin,
                             django.test.TestCase):
    url = reverse_lazy('ui:users:password_change')


class PasswordChangeDoneViewTest(RequiresAuthMixin, RendersTemplateMixin,
                                 django.test.TestCase):
    url = reverse_lazy('ui:users:password_change_done')
