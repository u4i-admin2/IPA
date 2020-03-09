from django.contrib import admin
import modeltranslation.admin

import core_types.admin
import prisoners.models


class PrisonerTimelineInline(modeltranslation.admin.TranslationStackedInline):
    model = prisoners.models.PrisonerTimeline
    max_num = 5
    extra = 0
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class PrisonerArrestInline(admin.StackedInline):
    model = prisoners.models.PrisonerArrest
    max_num = 5
    extra = 0
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class PrisonerDetentionInline(admin.StackedInline):
    model = prisoners.models.PrisonerDetention
    max_num = 5
    extra = 0
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class PrisonerSentenceInline(admin.StackedInline):
    model = prisoners.models.PrisonerSentence
    max_num = 5
    extra = 0
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class PrisonerRelationshipInline(admin.StackedInline):
    model = prisoners.models.PrisonerRelationship
    max_num = 5
    extra = 0
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS
    fk_name = 'prisoner'


class PrisonerAffiliationInline(admin.StackedInline):
    """ Describes relationship with an organisation """
    model = prisoners.models.PrisonerAffiliation
    max_num = 5
    extra = 0
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class PrisonerArrestAdmin(admin.ModelAdmin):
    list_display = ['prisoner', 'id']
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS
    inlines = [
        PrisonerSentenceInline,
        PrisonerDetentionInline,
    ]


class PrisonerDetentionAdmin(admin.ModelAdmin):
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class PrisonerSentenceAdmin(admin.ModelAdmin):
    list_display = ['arrest', 'judge']
    search_fields = ['arrest__prisoner__surname']
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class PrisonerAdmin(modeltranslation.admin.TabbedTranslationAdmin):
    inlines = [
        PrisonerArrestInline,
        PrisonerTimelineInline,
        PrisonerRelationshipInline,
        PrisonerAffiliationInline
    ]
    list_filter = ['ethnicity', 'religion', 'gender']
    search_fields = ['forename', 'surname']
    list_display = ['forename', 'surname', 'gender', 'needs_attention', 'is_published']
    list_editable = ['is_published']
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class DetentionStatusAdmin(modeltranslation.admin.TabbedTranslationAdmin):
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS
    list_display = ['id', 'name', 'detained']


admin.site.register(prisoners.models.ActivityPersecutedFor, core_types.admin.ChoiceAdmin)
admin.site.register(prisoners.models.ChargedWith, core_types.admin.ChoiceAdmin)
admin.site.register(prisoners.models.DetentionStatus, DetentionStatusAdmin)
admin.site.register(prisoners.models.DomesticLawViolated, core_types.admin.ChoiceAdmin)
admin.site.register(prisoners.models.InternationalLawViolated, core_types.admin.ChoiceAdmin)
admin.site.register(prisoners.models.Organisation, core_types.admin.ChoiceAdmin)
admin.site.register(prisoners.models.Prisoner, PrisonerAdmin)
admin.site.register(prisoners.models.PrisonerArrest, PrisonerArrestAdmin)
admin.site.register(prisoners.models.PrisonerDetention, PrisonerDetentionAdmin)
admin.site.register(prisoners.models.PrisonerSentence, PrisonerSentenceAdmin)
admin.site.register(prisoners.models.RelationshipType, core_types.admin.ChoiceAdmin)
admin.site.register(prisoners.models.PrisonTreatment, core_types.admin.ChoiceAdmin)

admin.site.register(prisoners.models.CaseId, core_types.admin.ChoiceAdmin)
