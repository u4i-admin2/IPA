"""
Common serializer functionality shared with all modules.
"""
import rest_framework.relations
import rest_framework.serializers


class UserSerializer(rest_framework.serializers.Serializer):
    """
    Serialize a django.contrib.auth user.

    We don't use ModelSerializer to avoid having to import so that we don't
    accidentally support modifying user objects.
    """
    class Meta:
        fields = (
            'username',
            'forename',
            'surname',
        )
        read_only_fields = fields

    username = rest_framework.serializers.CharField()
    forename = rest_framework.serializers.CharField(source='first_name')
    surname = rest_framework.serializers.CharField(source='last_name')


class PrimaryKeyIdRelatedField(rest_framework.relations.PrimaryKeyRelatedField):
    """
    Override PrimaryKeyRelatedField to return the actual integer primary key.
    """
    def to_internal_value(self, data):
        model = super(PrimaryKeyIdRelatedField, self).to_internal_value(data)
        return model.pk


class WritableManyManyField(rest_framework.relations.RelatedField):
    def to_internal_value(self, data):
        try:
            mgr = self.get_queryset().model.objects
            return [mgr.get(pk=p) for p in data]
        except TypeError:
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, many_many_manager):
        if hasattr(many_many_manager, 'all'):
            return [obj.pk for obj in many_many_manager.all()]
        else:
            return many_many_manager.pk


class ModelSerializer(rest_framework.serializers.ModelSerializer):
    """
    Override rest_framework ModelSerializer to support a new
    'writable_nested_fields' parameter. This parameter causes embedded
    serializers to automatically produce a second writeable field, which is the
    primary key of the nested object.

    This works around a limitation of rest_framework, allowing the (read-only)
    nested representation to be returned in GET requests, while still allowing
    REST clients to update the referenced object using the new writeable _id
    field during POSTs.

    Example:

        class PersonSerializer(api.serializers.ModelSerializer):
            address = AddressSerializer(read_only=True)
            class Meta:
                writable_nested_fields = (
                    'address',
                )

    Now Person JSON will look like:

        {
            'address': {
                'id': 1,
                'line1': '1 London Road',
            },
            'address_id': 1
        }

    And JavaScript can change the referenced address object using a POST like:

        {
            'address_id': 69
        }
    """

    def make_writable_nested_fields(self, fields):
        for name in getattr(self.Meta, 'writable_nested_fields', ()):
            field = fields[name]
            assert field.read_only is True, \
                ('You must set %s.%s read_only=True otherwise '
                 'rest_framework will throw exceptions during POST.'
                 % (type(self).__name__, name))

            fields[name + '_id'] = PrimaryKeyIdRelatedField(
                allow_null=field.allow_null,
                label=field.label,
                queryset=field.Meta.model.objects.all(),
                source=field.source,
                required=False)

    def make_writable_many_many_fields(self, fields):
        for name in getattr(self.Meta, 'writable_many_many_fields', ()):
            field = fields[name]
            assert field.read_only is True, \
                ('You must set %s.%s read_only=True otherwise '
                 'rest_framework will throw exceptions during POST.'
                 % (type(self).__name__, name))

            if name.endswith('_objs'):
                name = name[:-5]

            fields[name + '_ids'] = WritableManyManyField(
                allow_null=False,
                required=False,
                label=field.label,
                queryset=field.child.Meta.model.objects.all(),
                source=field.source or name,
            )

    def get_fields(self):
        fields = super(ModelSerializer, self).get_fields()
        self.make_writable_nested_fields(fields)
        self.make_writable_many_many_fields(fields)
        return fields
