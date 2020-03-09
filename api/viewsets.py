
import importlib

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
# import django.utils.image
from PIL import Image
import rest_framework.authentication
import rest_framework.exceptions
import rest_framework.filters
import rest_framework.pagination
import rest_framework.permissions
import rest_framework.response
import rest_framework.viewsets

import api.models
import api.renderers
import api.utils
import core_types.models


VIEWSETS = []


def register(name):
    """
    """
    module = importlib.import_module('%s.viewsets' % (name,))
    VIEWSETS.append((name, module.VIEWSETS))


def is_superuser(request):
    """
    Return True if the user in `request` is considered to be a super-user.
    """
    return any(g.name == settings.APP_SUPERUSER_GROUP_NAME
               for g in request.user.groups.all())


class UnpublishedReadRequiresAuth(rest_framework.permissions.BasePermission):
    """
    Veto the request if it involves accessing a PublishableMixin model,
    that model has not yet been published, and the requesting user has not
    authenticated.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access to things that aren't PublishableMixins, otherwise if
        # they are a PublishableMixin, only allow the request if the user is
        # logged in, or if the object is published.
        return ((not isinstance(obj, core_types.models.PublishableMixin)) or
                obj.is_published or
                (request.user and request.user.is_authenticated()))


class MyLimitOffsetPagination(rest_framework.pagination.LimitOffsetPagination):
    """
    Configure a default pagination limit of 25 items. This has the side effect
    of ensuring we always generate the "pagination format" output, which has
    next/previous/count/results fields.
    """
    default_limit = 25


class MySearchFilter(rest_framework.filters.SearchFilter):
    """
    Override the default SearchFilter query string parameter name, to avoid
    having to change the front-end.
    """
    search_param = "q"


class RestrictedQuerySetMixin(object):
    """
    Override the default get_queryset() to automatically exclude
    unpublished items if the requesting user is not authenticated.

    Also related to https://github.com/smallmedia/united/issues/84
    """
    def get_queryset(self):
        qs = super(RestrictedQuerySetMixin, self).get_queryset()
        if issubclass(qs.model, core_types.models.PublishableMixin) and \
                not (self.request.user and self.request.user.is_authenticated()):
            qs = qs.exclude(is_published=False)

        return qs


class PermissionsMixin(object):
    authentication_classes = [
        rest_framework.authentication.BasicAuthentication,
        rest_framework.authentication.SessionAuthentication,
    ]

    permission_classes = [
        rest_framework.permissions.IsAuthenticated,
        # rest_framework.permissions.IsAuthenticatedOrReadOnly,
        # UnpublishedReadRequiresAuth,
    ]


class ModelViewSet(PermissionsMixin,
                   rest_framework.viewsets.ModelViewSet):
    """
    Override the default rest_framework ModelViewSet to integrate its
    authentication/permissions system with our app, namely:

        * Authenticate users via django.contrib.auth.

        * Authorize modifications depending on the user's group and whether
          PublishedMixin.is_published is True or False.

        * Prevent non-superusers from marking published existing models, or
          creating new models that are marked published.
    """
    filter_backends = [
        rest_framework.filters.OrderingFilter,
        MySearchFilter,
    ]

    pagination_class = MyLimitOffsetPagination
    search_fields = ()

    def perform_create(self, serializer):
        """
        Veto the request if it is attempting to create a model with
        is_published=True, and the user is not an administrator.
        """
        if serializer.validated_data.get('is_published') and \
                not is_superuser(self.request):
            msg = ("Your account does not have permission to create "
                   "published objects; please ask a member of the "
                   "%r group to make this change for you."
                   % (settings.APP_SUPERUSER_GROUP_NAME,))
            raise rest_framework.exceptions.PermissionDenied(msg)

        return super(ModelViewSet, self).perform_create(serializer)

    def perform_update(self, serializer):
        """
        Veto the request if it involves an edit to a PublishableMixin model,
        and that model is marked as published=True, and the editing user is not
        an administrator.
        """
        if serializer.instance.is_published and not is_superuser(self.request):
            msg = ("Your account does not have permission to edit "
                   "published objects; please ask a member of the "
                   "%r group to make this change for you."
                   % (settings.APP_SUPERUSER_GROUP_NAME,))
            raise rest_framework.exceptions.PermissionDenied(msg)

        return super(ModelViewSet, self).perform_update(serializer)


class ChoiceViewSet(ModelViewSet):
    """
    Like ModelViewSet, except configure search_fields automatically.
    """
    search_fields = (
        'name_en',
        'name_fa',
    )


class ImageUploadViewSet(RestrictedQuerySetMixin,
                         PermissionsMixin,
                         rest_framework.viewsets.GenericViewSet):
    """
    Allow uploading just the file part of some model, without affecting its
    related fields.
    """
    #: Set me in your subclass!
    base_name = 'pictures'

    #: Set me in your subclass!
    image_field_name = 'picture'

    serializer_class = rest_framework.serializers.Serializer

    def list(self, request, **kwargs):
        """
        Return a dummy list result just so we show up in the API browser.
        """
        msg = _('Items of this collection can only be updated, the '
                'collection itself cannot be browsed or retrieved from.')
        raise rest_framework.exceptions.PermissionDenied(msg)

    retrieve = list

    def post(self, request, **kwargs):
        """
        Handle file upload by replacing the existing Judge photo.
        """
        if not request.FILES:
            msg = _('No file specified.')
            raise rest_framework.exceptions.ParseError(msg)

        fileobj = request.FILES[request.FILES.keys()[0]]
        try:
            # django.utils.image.Image.open(fileobj).verify()
            Image.open(fileobj).verify()
        except Exception:
            return rest_framework.response.Response({
                'detail': _('The uploaded file was not an image.'),
            }, status=400)

        fileobj.seek(0)
        instance = self.get_object()
        setattr(instance, self.image_field_name, fileobj)
        instance.save()

        return rest_framework.response.Response({
            'url': getattr(instance, self.image_field_name).url
        })


class TagListViewSet(rest_framework.viewsets.GenericViewSet):
    """
    This pretends to be a ViewSet over TagList models, however we override the
    list() and retrieve() methods to always return the same thing: a list of
    field descriptions extracted from the models defined in MODEL_NAME.

    This allows the ViewSet to be used with the regular rest_framework
    DefaultRouter, keeping everything fairly neat and tidy, instead of mixing
    custom url()/DefaultRouter() based routing.
    """
    # TagList models are never actually created. This is purely to trick
    # DefaultRouter.
    queryset = api.models.TagList.objects.all()

    #: Set me to a module name in your subclass.
    MODULE_NAME = None

    def retrieve(self, request, pk=None):
        """
        Use api.utils.extract_model_fields() to build a list of field tags for
        MODULE_NAME, then return that as a rest_framework Response.
        """
        tag_list = sorted(api.utils.extract_model_fields(self.MODULE_NAME))
        return rest_framework.response.Response(tag_list)

    # list() and retrieve() do exactly the same thing.
    list = retrieve
