"""
Editable Types
"""

from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

from core_types.translation import ChoiceTranslationOptions
from core_types.translation import QuoteTranslationOptions
from core_types.translation import FileTranslationOptions
from core_types.translation import TimelineTranslationOptions
from . import models


class PrisonerTranslationOptions(TranslationOptions):
    fields = (
        'forename',
        'surname',
        'biography',
    )


class PrisonerRelationshipTranslationOptions(TranslationOptions):
    fields = (
        'forename',
        'surname',
    )


class SentenceBehaviourTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )


class PrisonerSentenceTranslationOptions(TranslationOptions):
    fields = (
        'social_depravation',
    )


translator.register(models.ActivityPersecutedFor, ChoiceTranslationOptions)
translator.register(models.CaseId, ChoiceTranslationOptions)
translator.register(models.ChargedWith, ChoiceTranslationOptions)
translator.register(models.DetentionStatus, ChoiceTranslationOptions)
translator.register(models.DomesticLawViolated, ChoiceTranslationOptions)
translator.register(models.InternationalLawViolated, ChoiceTranslationOptions)
translator.register(models.Organisation, ChoiceTranslationOptions)
translator.register(models.PrisonTreatment, ChoiceTranslationOptions)
translator.register(models.Prisoner, PrisonerTranslationOptions)
translator.register(models.PrisonerFile, FileTranslationOptions)
translator.register(models.PrisonerQuote, QuoteTranslationOptions)
translator.register(models.PrisonerRelationship, PrisonerRelationshipTranslationOptions)
translator.register(models.PrisonerTimeline, TimelineTranslationOptions)
translator.register(models.RelationshipType, ChoiceTranslationOptions)
translator.register(models.SentenceBehaviour, SentenceBehaviourTranslationOptions)
translator.register(models.PrisonerSentence, PrisonerSentenceTranslationOptions)
