from django.contrib import admin
import modeltranslation.admin

import core_types.admin
import prisons.models


class PrisonAdmin(modeltranslation.admin.TabbedTranslationAdmin):
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


class PrisonFacilityAdmin(modeltranslation.admin.TabbedTranslationAdmin):
    readonly_fields = core_types.admin.PUBLISHABLE_READONLY_FIELDS


admin.site.register(prisons.models.Prison, PrisonAdmin)
admin.site.register(prisons.models.PrisonFacility, PrisonAdmin)
