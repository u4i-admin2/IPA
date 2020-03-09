from django.contrib import admin

from django import forms
# from redactor.widgets import RedactorEditor
from adminsortable.admin import SortableAdmin
from modeltranslation.admin import TranslationAdmin
from image_cropping import ImageCropWidget
from models import Page


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        widgets = {
            # 'content_fa': RedactorEditor(),
            # 'content_en': RedactorEditor(),
            'image': ImageCropWidget,
        }
        exclude = []


class PageAdmin(TranslationAdmin, SortableAdmin):
    form = PageAdminForm
    list_display = ['slug', 'title', 'modified_date', 'order']
    exclude = []


admin.site.register(Page, PageAdmin)
