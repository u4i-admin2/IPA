
from django.conf import settings
import django.db.models.fields.files
import easy_thumbnails.files
import easy_thumbnails.exceptions
import rest_framework.fields


class ForcedRangeIntegerField(rest_framework.fields.IntegerField):
    forced_min_value = None
    forced_max_value = None

    # Needed to work around a rest_framework bug.
    default_error_messages = {
        'max_value': 'Ensure this value is less than or equal to {max_value}.',
        'min_value': 'Ensure this value is greater than or equal to {min_value}.',
    }

    def __init__(self, *args, **kwargs):
        kwargs['min_value'] = self.forced_min_value
        kwargs['max_value'] = self.forced_max_value
        kwargs['allow_null'] = True
        kwargs['required'] = False
        super(ForcedRangeIntegerField, self).__init__(*args, **kwargs)


class GregorianYearField(ForcedRangeIntegerField):
    forced_min_value = 1800
    forced_max_value = 2200


class GregorianMonthField(ForcedRangeIntegerField):
    forced_min_value = 1
    forced_max_value = 12


class GregorianDayField(ForcedRangeIntegerField):
    forced_min_value = 1
    forced_max_value = 31


class FarsiYearField(ForcedRangeIntegerField):
    forced_min_value = 1180
    forced_max_value = 1580


class FarsiMonthField(ForcedRangeIntegerField):
    forced_min_value = 1
    forced_max_value = 12


class FarsiDayField(ForcedRangeIntegerField):
    forced_min_value = 1
    forced_max_value = 31


class ThumbnailImageField(rest_framework.fields.Field):
    """
    This field expects its source= to be a django.db.models.ImageField
    containing an image it will return a thumbnail URL for. The size of the
    generated thumbnail comes from settings.API_THUMB_SIZE.
    """
    def __init__(self, size=settings.API_THUMB_SIZE, **kwargs):
        kwargs['read_only'] = True
        super(ThumbnailImageField, self).__init__(**kwargs)

        self.options = {
            'upscale': True,
            'size': size,
            'crop': 'smart'
        }

    def to_representation(self, source):
        assert isinstance(source,
                          django.db.models.fields.files.ImageFieldFile), \
            'ThumbnailImageField only works with ImageFields.'

        if source:
            thumbnailer = easy_thumbnails.files.get_thumbnailer(source)
            try:
                return thumbnailer.get_thumbnail(self.options).url
            except easy_thumbnails.exceptions.InvalidImageFormatError:
                pass
            except IOError:
                pass
            except UnicodeEncodeError:
                pass
