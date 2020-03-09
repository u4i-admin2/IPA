"""
Editable Types
"""

from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

from core_types.translation import ChoiceTranslationOptions
from core_types.translation import FileTranslationOptions
from core_types.translation import QuoteTranslationOptions
from core_types.translation import TimelineTranslationOptions
from . import models


class PrisonTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'address',
        'dean_name',
        'physical_structure',
        'size_and_density',
        'medicine_and_nutrition',
        'bio',
    )


class FacilityLinkTranslationOptions(TranslationOptions):
    fields = ('description',)


translator.register(models.Prison, PrisonTranslationOptions)
translator.register(models.PrisonFacility, ChoiceTranslationOptions)
translator.register(models.PrisonQuote, QuoteTranslationOptions)
translator.register(models.PrisonFile, FileTranslationOptions)
translator.register(models.PrisonTimeline, TimelineTranslationOptions)
translator.register(models.PrisonFacilityLink, FacilityLinkTranslationOptions)
