from django.contrib import admin
import modeltranslation.admin

import core_types.admin
import judges.models


class JudgePositionInline(admin.StackedInline):
    model = judges.models.JudgePosition
    max_num = 5
    extra = 0
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class JudgeQuoteInline(modeltranslation.admin.TranslationStackedInline):
    model = judges.models.JudgeQuote
    max_num = 5
    extra = 0
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class TimelineJudgeInline(modeltranslation.admin.TranslationStackedInline):
    model = judges.models.JudgeTimeline
    max_num = 5
    extra = 0
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class JudgeAdmin(modeltranslation.admin.TabbedTranslationAdmin):
    inlines = [JudgePositionInline, JudgeQuoteInline, TimelineJudgeInline]
    list_display = ['__unicode__', 'is_judge']
    list_editable = ['is_judge']
    search_fields = ['forename', 'surname']
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class SentenceTypeAdmin(modeltranslation.admin.TabbedTranslationAdmin):
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


admin.site.register(judges.models.CourtAndBranch, core_types.admin.ChoiceAdmin)
admin.site.register(judges.models.Judge, JudgeAdmin)
admin.site.register(judges.models.BehaviourType, core_types.admin.ChoiceAdmin)
admin.site.register(judges.models.JudicialPosition, core_types.admin.ChoiceAdmin)
admin.site.register(judges.models.SentenceType, SentenceTypeAdmin)
