"""
Editable Types
"""

from modeltranslation.translator import translator
from models import (
    HumanRightViolated,
    ReportQuote,
    ReportFile,
)
from core_types.translation import (
    ChoiceTranslationOptions,
    QuoteTranslationOptions,
    FileTranslationOptions,
)


translator.register(HumanRightViolated, ChoiceTranslationOptions)
translator.register(ReportQuote, QuoteTranslationOptions)
translator.register(ReportFile, FileTranslationOptions)
