from modeltranslation.translator import translator, TranslationOptions
from models import Page


class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(Page, PageTranslationOptions)
