from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

from core_types.translation import ChoiceTranslationOptions
from core_types.translation import FileTranslationOptions
from core_types.translation import QuoteTranslationOptions
from core_types.translation import TimelineTranslationOptions
from . import models


class JudgeTranslationOptions(TranslationOptions):
    fields = (
        'forename',
        'surname',
        'biography',
    )


translator.register(models.BehaviourType, ChoiceTranslationOptions)
translator.register(models.CourtAndBranch, ChoiceTranslationOptions)
translator.register(models.Judge, JudgeTranslationOptions)
translator.register(models.JudgeFile, FileTranslationOptions)
translator.register(models.JudgeQuote, QuoteTranslationOptions)
translator.register(models.JudgeTimeline, TimelineTranslationOptions)
translator.register(models.JudicialPosition, ChoiceTranslationOptions)
translator.register(models.SentenceType, ChoiceTranslationOptions)
