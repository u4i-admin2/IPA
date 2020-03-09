from django.contrib import admin
import modeltranslation.admin

import core_types.models

PUBLISHABLE_READONLY_FIELDS = [
    'created',
    'updated',
    'created_by',
    'updated_by',
]


class ChoiceAdmin(modeltranslation.admin.TabbedTranslationAdmin):
    search_fields = ['name']
    list_display = ['name']
    readonly_fields = PUBLISHABLE_READONLY_FIELDS


class CityAdmin(ChoiceAdmin):
    list_filter = ['province', 'located_in_iran']
    list_display = ChoiceAdmin.list_display + ['province', 'located_in_iran']


admin.site.register(core_types.models.City, CityAdmin)
admin.site.register(core_types.models.Country, ChoiceAdmin)
admin.site.register(core_types.models.Ethnicity, ChoiceAdmin)
admin.site.register(core_types.models.Province, ChoiceAdmin)
admin.site.register(core_types.models.Religion, ChoiceAdmin)
