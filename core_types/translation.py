from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

from . import models


class ChoiceTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


class QuoteTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'quote',
    )


class FileTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )


class TimelineTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )


translator.register(models.City, ChoiceTranslationOptions)
translator.register(models.Country, ChoiceTranslationOptions)
translator.register(models.Ethnicity, ChoiceTranslationOptions)
translator.register(models.Province, ChoiceTranslationOptions)
translator.register(models.Religion, ChoiceTranslationOptions)
