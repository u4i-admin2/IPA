
import datetime
import inspect

from django.db import models
from django.utils.module_loading import import_string
import django.http
import modeltranslation.fields

import core_types.models


EXCLUDE_FIELD_NAMES = (
    'id',
    'is_published',
    'updated',
    'updated_by',
    'created',
    'created_by',
)


def walk_model_fields(model_class):
    """
    Return a list describing all the fields of `model_class`. The returned list
    contains tuples like `(type, field_name, related_model_class)`, where:

        type: one of "field", "foreign_key", "many_to_many", or "related",
        depending on how the field is related to this model.

        field_name: the name of the attribute on this model for accessing the
        field.

        related_model_class: for types other than "field", this is the class of
        the related model class. For example:

                foo = models.ForeignKey('FooBar')

            would be:
                [('foreign_key', 'foo', FooBar)]
    """
    out = []

    for field in model_class._meta.concrete_fields:
        if isinstance(field, models.ForeignKey):
            out.append(('foreign_key', field.name, field.remote_field.parent_link))
        else:
            out.append(('field', field.name, None))

    for field in model_class._meta.many_to_many:
        out.append(('many_to_many', field.name, field.remote_field.parent_link))

    for rel in model_class._meta.get_fields():
        if (rel.one_to_many or rel.one_to_one) and rel.auto_created and not rel.concrete:
            out.append(('related', rel.get_accessor_name(), rel.model))

    return out


def extract_model_fields(modname):
    """
    Given a string module name, find all the Model subclasses defined in it,
    then build up a set of friendly strings representing all the possible field
    tags that might apply to the models from that module.

    Example:

        >>> extract_model_fields('my.module')
        set(['Prisoner: Name', 'Prisoner: Age'])
    """
    module = import_string(modname)
    out = []

    EXCLUDE_MODEL_CLASSES = (
        core_types.models.Source,
        core_types.models.Comment,
    )

    EXCLUDE_FIELD_CLASSES = (
        modeltranslation.fields.TranslationField,
        models.ManyToManyField,
    )

    for name, model in vars(module).iteritems():
        if not (inspect.isclass(model) and
                issubclass(model, models.Model) and
                not issubclass(model, EXCLUDE_MODEL_CLASSES)):
            continue

        fields = model._meta.fields
        # field_names = set(f.name for f in fields)

        for field in fields:
            if not (isinstance(field, EXCLUDE_FIELD_CLASSES) or
                    field.name in EXCLUDE_FIELD_NAMES or
                    field.verbose_name[0].islower()):
                name = u'%s: %s' % (model._meta.verbose_name,
                                    field.verbose_name)
                out.append(name)

    return sorted(out)


def datetime_from_javascript(ms):
    """
    Return a datetime given the number of milliseconds since January 1, 1970
    (aka. JavaScript "new Date(ms)" format).
    """
    secs, ms = divmod(ms, 1000.0)
    dt = datetime.datetime.fromtimestamp(secs)
    return dt.replace(microsecond=int(ms * 1000.0))


UNIX_EPOCH_DT = datetime.datetime(1970, 1, 1)


def datetime_to_javascript(dt):
    """
    Convert a datetime to the number of milliseconds since January 1, 1970
    (aka. JavaScript "new Date(ms)" format).
    """
    return (dt.replace(tzinfo=None) - UNIX_EPOCH_DT).total_seconds() * 1000.0


def get_request():
    """
    Walk up the stack, return the nearest first argument named "request".

    http://nedbatchelder.com/blog/201008/global_django_requests.html
    """
    frame = None
    try:
        for frame, _, _, _, _, _ in inspect.stack():
            request = frame.f_locals.get('request')
            if request and isinstance(request, django.http.HttpRequest):
                return request
    finally:
        del frame


def get_request_user():
    request = get_request()
    if request:
        return request.user


def absolute_urljoin(suffix):
    request = get_request()
    if request:
        return request.build_absolute_uri(suffix)
    return suffix
