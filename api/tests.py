
import pprint
import tempfile

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
import modeltranslation.translator
import django.contrib.auth.models
import rest_framework.serializers
import rest_framework.test

import api.models
import core_types.models


request_factory = rest_framework.test.APIRequestFactory()

ONE_X_ONE_GIF = (
    '47494638396101000100800100ff0000ffffff21f90'
    '401000001002c00000000010001000002024401003b'
).decode('hex')


class TestCase(rest_framework.test.APITestCase):
    """
    Base class for our test cases. May be used later to configure/add helper
    functionality.
    """
    from model_mommy import mommy


class UserAccountsMixin(object):
    @classmethod
    def setUpClass(cls):
        super(UserAccountsMixin, cls).setUpClass()
        cls.superuser = django.contrib.auth.models.User.objects.create_superuser(
            username='admin_user',
            email='admin_user',
            password='admin_user')

        cls.user = django.contrib.auth.models.User.objects.create_superuser(
            username='user',
            email='user',
            password='user')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.superuser.delete()
        super(UserAccountsMixin, cls).tearDownClass()


class BaseViewSetMixin(object):
    """
    Mix me into your API view test class after setting various attributes below
    to test basic API serializer/viewset functionality.
    """
    viewset_class = None    # e.g. core_types.viewsets.ProvinceViewSet
    name_prefix = None      # e.g. api:province, see ./manage.py show_urls

    #
    # Model factory function.
    #

    def make_model(self, **kwargs):
        """
        The default implementation tries to use Model Mommy to automatically
        create an instance of the model and all its dependents. If this doesn't
        work, just override the method in your subclass.
        """
        kwargs.update(self.get_mommy_extra_args())
        return self.mommy.make(self.viewset_class.queryset.model, **kwargs)

    def make_dummy_json(self, **kwargs):
        """
        Return a JSON dict describing a dummy non-existent model, serialized
        using the ViewSet's configured serializer. This JSON should be POSTable
        to the collection without causing errors.

        The side effect of this implementation is that if your serializer is
        missing fields, you won't be able to save any new models after a POST.
        In other words, it helps test the serializer too.
        """
        mod = self.make_model(**kwargs)
        request = request_factory.get('/')
        json = self.serializer_class(instance=mod, context={'request': request}).data
        json.update(self.get_extra_json_data())
        mod.delete()
        del json['id']
        pprint.pprint(dict(json))
        return json

    def get_mommy_extra_args(self):
        """
        Override this function to provide extra arguments to Model Mommy.
        """
        return {}

    def get_extra_json_data(self):
        """
        Override this function to provide extra JSON POST dictionary contents.
        """
        return {}

    #
    # ViewSet helpers.
    #

    @property
    def serializer_class(self):
        return self.viewset_class.serializer_class

    @property
    def model_class(self):
        return self.serializer_class.queryset.model

    #
    # URL helpers.
    #

    def url(self, suffix, **kwargs):
        return reverse('%s-%s' % (self.name_prefix, suffix), kwargs=kwargs)

    def list_url(self):
        return self.url('list')

    def detail_url(self, pk):
        return self.url('detail', pk=pk)


class ViewSetMixin(UserAccountsMixin, BaseViewSetMixin):
    """
    Mix me into your API view test class after setting various attributes below
    to test basic API serializer/viewset functionality.
    """

    #
    # List tests.
    #

    def test_auth_needed(self):
        resp = self.client.get(self.list_url())
        self.assertEquals(resp.status_code, 401)

    def test_list_empty(self):
        self.client.login(username=self.user.username, password=self.user.username)
        resp = self.client.get(self.list_url())
        self.assertEquals([], resp.data['results'])

    def test_list_exists(self):
        mod = self.make_model()
        if hasattr(mod, 'is_published'):
            mod.is_published = True
            mod.save()
        self.client.login(username=self.user.username, password=self.user.username)
        resp = self.client.get(self.list_url())
        self.assertNotEquals([], resp.data['results'])
        self.assertEquals(mod.pk, resp.data['results'][0]['id'])

    #
    # PublishableMixin behaviour tests.
    # Deprecated as now api is authentication only

    # def test_publishable_list_hidden_if_anonymous(self):
    #     # This is testing api.viewsets.RestrictedQuerySetMixin.
    #     mod = self.make_model()
    #     if not isinstance(mod, core_types.models.PublishableMixin):
    #         return

    #     # is_published defaults to False.
    #     resp = self.client.get(self.list_url())
    #     self.assertEquals([], resp.data['results'])

    #     mod.is_published = True
    #     mod.save()

    #     resp = self.client.get(self.list_url())
    #     self.assertNotEquals([], resp.data['results'])
    #     self.assertEquals(mod.pk, resp.data['results'][0]['id'])

    #     mod.is_published = False
    #     mod.save()

    #     resp = self.client.get(self.list_url())
    #     self.assertEquals([], resp.data['results'])

    #     self.client.login(username=self.user.username,
    #                       password=self.user.username)
    #     resp = self.client.get(self.list_url())
    #     self.assertNotEquals([], resp.data['results'])
    #     self.assertEquals(mod.pk, resp.data['results'][0]['id'])

    # def test_publishable_detail_404_if_anonymous(self):
    #     # This is testing api.viewsets.RestrictedQuerySetMixin.
    #     mod = self.make_model()
    #     if not isinstance(mod, core_types.models.PublishableMixin):
    #         return

    #     # is_published defaults to False.
    #     resp = self.client.get(self.detail_url(mod.pk))
    #     self.assertEquals(404, resp.status_code)

    #     mod.is_published = True
    #     mod.save()

    #     resp = self.client.get(self.detail_url(mod.pk))
    #     self.assertEquals(200, resp.status_code)

    # publishable_child_relation_name = None
    # def make_publishable_child_relation_model(self):
    #     pass

    # def test_publishable_children_hidden(self):
    #     # This is testing core_types.serializers.PublishableListSerializer.
    #     # Subclasses must set publishable_child_relation_name and
    #     # publishable_child_relation_model for it to run. See judges/tests.py
    #     # for example.
    #     if not self.publishable_child_relation_name:
    #         return

    #     mod = self.make_model(is_published=True)
    #     child = self.make_publishable_child_relation(mod)

    #     # First check the relation list is empty for anonymous users.
    #     resp = self.client.get(self.detail_url(mod.pk))
    #     self.assertEquals(resp.status_code, 200)
    #     self.assertEquals([], resp.data[self.publishable_child_relation_name])

    #     # Now login and see if it shows up for authenticated users.
    #     self.client.login(username=self.user.username,
    #                       password=self.user.username)

    #     resp = self.client.get(self.detail_url(mod.pk))
    #     self.assertEquals(resp.status_code, 200)
    #     self.assertNotEquals([], resp.data[self.publishable_child_relation_name])
    #     self.assertEquals(child.pk,
    #                      resp.data[self.publishable_child_relation_name][0]['id'])

    #
    # Retrieve tests.
    #

    def test_detail_exists(self):
        mod = self.make_model()
        self.client.login(username=self.user.username,
                          password=self.user.username)
        resp = self.client.get(self.detail_url(pk=mod.pk))
        self.assertEquals(resp.data['id'], mod.pk)
        self.assertTrue(resp.data['url'].endswith(self.detail_url(pk=mod.pk)))

    def get_field_list(self, model):
        names = set(f.name for f in model._meta.concrete_fields)

        # Now update the set to account for translated fields.
        try:
            opts = (modeltranslation.translator
                    .translator.get_options_for_model(model))
        except modeltranslation.translator.NotRegistered:
            return names

        for source_field, trans_fields in opts.fields.iteritems():
            names.remove(source_field)
            names.update(f.name for f in trans_fields)
        return names

    def test_detail_fields_populated(self):
        """
        Ensure the API output actually contains a dictionary key for every
        field in the associated Model class.
        """
        mod = self.make_model()
        self.client.login(username=self.user.username,
                          password=self.user.username)
        resp = self.client.get(self.detail_url(pk=mod.pk))

        hidden = getattr(self.serializer_class.Meta, 'api_hidden_fields', ())
        for field_name in self.get_field_list(type(mod)):
            self.assertTrue((field_name in hidden) or
                            (field_name in resp.data) or
                            (field_name + '_id' in resp.data) or
                            # These four aren't present unless ?verbose=1.
                            (field_name in ('created_by', 'updated_by', 'created', 'updated')),
                            'Field %r of %r is neither present in '
                            '%s.Meta.api_hidden_fields nor present in '
                            'the serializer\'s output.' % (
                                field_name,
                                self.viewset_class,
                                self.serializer_class.__name__))

    #
    # Serializer validation tests.
    #

    def test_year_month_day_fields_have_min_max_value(self):
        for name, field in self.serializer_class().fields.iteritems():
            if name.endswith('year'):
                self.assertEquals(field.min_value, 1800, name)
                self.assertEquals(field.max_value, 2200, name)
            elif name.endswith('year_fa'):
                self.assertEquals(field.min_value, 1180, name)
                self.assertEquals(field.max_value, 1580, name)
            elif name.endswith('month') or name.endswith('month_fa'):
                self.assertEquals(field.min_value, 1, name)
                self.assertEquals(field.max_value, 12, name)
            elif name.endswith('day') or name.endswith('day_fa'):
                self.assertEquals(field.min_value, 1, name)
                self.assertEquals(field.max_value, 31, name)

    #
    # Create/update/delete tests.
    #

    post_format = 'json'

    def test_creates_fails_unauthenticated(self):
        json = self.make_dummy_json()
        resp = self.client.post(self.list_url(), json,
                                format=self.post_format)
        self.assertEquals(401, resp.status_code)

    def test_can_create(self):
        self.client.login(username=self.user.username,
                          password=self.user.username)
        json = self.make_dummy_json()
        resp = self.client.post(self.list_url(), json,
                                format=self.post_format)
        if resp.status_code != 201:
            pprint.pprint(vars(resp))
        self.assertEquals(201, resp.status_code)

    def test_list_field_configs(self):
        """
        many=True embedded serializers must always have read_only=True, else
        rest_framework complains during create().
        """
        for name, field in self.serializer_class().fields.items():
            if isinstance(field, rest_framework.serializers.ListSerializer):
                self.assertTrue(field.read_only, name)

    def get_nested_fields(self):
        return [(name, fld)
                for name, fld in self.serializer_class().fields.items()
                if isinstance(fld, rest_framework.serializers.BaseSerializer)]

    def test_nested_field_configs(self):
        """
        Ensure nested serializers are configured to be read-only, else
        rest_framework complains during create().
        """
        for name, field in self.get_nested_fields():
            self.assertTrue(field.read_only, name)

    def test_nested_field_posts(self):
        """
        Ensure that POSTs to fields mentioned in Meta.writable_nested_fields
        update the relevant nested field. See
        api/serializers.py:ModelSerializer.create().
        """
        self.client.login(username=self.user.username,
                          password=self.user.username)
        json = self.make_dummy_json()
        resp = self.client.post(self.list_url(), json,
                                format=self.post_format)
        self.assertEquals(201, resp.status_code)

        json = resp.data
        writable_nested_fields = getattr(self.serializer_class.Meta,
                                         'writable_nested_fields', ())
        for name, field in self.get_nested_fields():
            if name in writable_nested_fields:
                # Now create a dummy nested model and try to set it on our instance
                # with POST.
                nested_model = self.mommy.make(field.Meta.model)
                json[name + '_id'] = nested_model.pk

                resp = self.client.put(self.detail_url(json['id']), json,
                                       format=self.post_format)
                self.assertEquals(200, resp.status_code)

                resp = self.client.get(self.detail_url(json['id']))
                self.assertEquals(200, resp.status_code)
                self.assertEquals(nested_model.pk, resp.data[name + '_id'],
                                  '%r_id != %d' % (name, nested_model.pk))
                self.assertTrue(resp.data[name] is not None,
                                '%r field was None in response' % (name,))
                self.assertEquals(nested_model.pk, resp.data[name]['id'])

    #
    # Test ManyToManyField writability.
    #

    def test_many_many_field_posts(self):
        self.client.login(username=self.user.username,
                          password=self.user.username)
        json = self.make_dummy_json()

        resp = self.client.post(self.list_url(), json,
                                format=self.post_format)
        self.assertEquals(201, resp.status_code)

        json = resp.data

        writable_many_many_fields = getattr(self.serializer_class.Meta,
                                            'writable_many_many_fields', ())
        for name, field in self.get_nested_fields():
            if name in writable_many_many_fields:
                # Now create a dummy nested model and try to set it on our instance
                # with POST.
                nested_model = self.mommy.make(field.child.Meta.model)
                ids_name = name[:-5] + '_ids'
                json[ids_name] = [nested_model.pk]

                from pprint import pprint
                pprint(json)

                resp = self.client.put(self.detail_url(json['id']), json,
                                       format=self.post_format)
                self.assertEquals(200, resp.status_code)

                resp = self.client.get(self.detail_url(json['id']))
                self.assertEquals(200, resp.status_code)
                self.assertEquals([nested_model.pk], resp.data[ids_name])
                self.assertNotEquals([], resp.data[name],
                                     '%r field was empty in response' % (name,))
                self.assertEquals(nested_model.pk, resp.data[name][0]['id'])

    #
    # Ensure PublishableMixin fields aren't writable.
    #

    def test_publishable_fields_readonly(self):
        if isinstance(self.viewset_class.queryset.model,
                      core_types.models.PublishableMixin):
            fields = self.serializer_class().fields
            self.assertTrue(fields['created'].read_only)
            self.assertTrue(fields['updated'].read_only)
            self.assertTrue(fields['created_by'].read_only)
            self.assertTrue(fields['updated_by'].read_only)


class ChoiceViewSetMixin(ViewSetMixin):
    """
    Mix me into your api.views.ChoiceViewSet test class.
    """

    #
    # Test q= parameter.
    #

    def test_autocomplete(self):
        # We must login so is_published=True stuff shows up.
        self.client.login(username=self.user.username,
                          password=self.user.username)

        mod1 = self.make_model(name_en='mod1_en', name_fa='mod1_fa')
        mod2 = self.make_model(name_en='mod2_en', name_fa='mod2_fa')

        resp = self.client.get(self.list_url() + '?q=charles')
        self.assertEquals(0, len(resp.data['results']))

        resp = self.client.get(self.list_url() + '?q=mod1_en')
        self.assertEquals(mod1.id, resp.data['results'][0]['id'])
        resp = self.client.get(self.list_url() + '?q=mod1_fa')
        self.assertEquals(mod1.id, resp.data['results'][0]['id'])

        resp = self.client.get(self.list_url() + '?q=mod2_en')
        self.assertEquals(mod2.id, resp.data['results'][0]['id'])
        resp = self.client.get(self.list_url() + '?q=mod2_fa')
        self.assertEquals(mod2.id, resp.data['results'][0]['id'])


class ImageUploadViewSetMixin(UserAccountsMixin, BaseViewSetMixin):
    def get_field(self, mod):
        return getattr(mod, self.viewset_class.image_field_name)

    def test_not_an_image(self):
        self.client.login(username=self.user.username,
                          password=self.user.username)

        mod = self.make_model()
        self.assertFalse(self.get_field(mod))

        with tempfile.NamedTemporaryFile() as fp, \
                tempfile.NamedTemporaryFile() as thumb_fp:
            fp.write('this is not an image')
            fp.seek(0)
            thumb_fp.write('this is not an image')
            thumb_fp.seek(0)
            resp = self.client.post(self.detail_url(mod.pk), {
                'file': fp,
                'file_thumb': thumb_fp,
            })

        self.assertEquals(400, resp.status_code)

    def test_image_upload(self):
        self.client.login(username=self.user.username,
                          password=self.user.username)

        mod = self.make_model()
        self.assertFalse(self.get_field(mod))

        with tempfile.NamedTemporaryFile() as fp, \
                tempfile.NamedTemporaryFile() as thumb_fp:
            fp.write(ONE_X_ONE_GIF)
            fp.seek(0)
            thumb_fp.write(ONE_X_ONE_GIF)
            thumb_fp.seek(0)
            resp = self.client.post(self.detail_url(mod.pk), {
                'file': fp,
                'file_thumb': thumb_fp,
            })

        self.assertEquals(200, resp.status_code)
        self.assertTrue('url' in resp.data)

        # Reload the model and ensure the file was uploaded.
        mod = type(mod).objects.get(pk=mod.pk)
        self.assertTrue(self.get_field(mod))


class FileUploadViewSetMixin(object):
    post_format = 'multipart'

    def get_extra_json_data(self):
        fp = tempfile.NamedTemporaryFile()
        thumb_fp = tempfile.NamedTemporaryFile()

        fp.write('test1')
        fp.seek(0)

        thumb_fp.write(ONE_X_ONE_GIF)
        thumb_fp.seek(0)
        return {
            'file': fp,
            'file_thumb': thumb_fp,
        }


class TaglistViewSetMixin(BaseViewSetMixin):
    def test_taglist_get(self):
        resp = self.client.get(self.list_url())
        self.assertEquals(200, resp.status_code)


class SearchViewSetTest(TestCase):
    """
    Test the basic Watson search API endpoint.
    """
    url = reverse_lazy('api:search-list')

    def test_search_no_q(self):
        resp = self.client.get(self.url)
        self.assertEquals(400, resp.status_code)

    def test_search_no_results(self):
        resp = self.client.get(self.url + '?q=nonexistent')
        self.assertEquals(200, resp.status_code)
        self.assertEquals([], resp.data)

    class SearchTestModelSerializer(rest_framework.serializers.Serializer):
        id = rest_framework.serializers.IntegerField()
        url = rest_framework.serializers.CharField()

    def test_has_results(self):
        api.search.register(api.models.SearchTestModel,
                            self.SearchTestModelSerializer)

        stm = api.models.SearchTestModel()
        stm.text = 'this-definitely-exists'
        stm.save()

        resp = self.client.get(self.url + '?q=definitely')
        self.assertEquals(200, resp.status_code)
        self.assertEquals(1, len(resp.data))
        self.assertEquals(stm.id, resp.data[0]['id'])
        self.assertEquals(stm.url, resp.data[0]['url'])
