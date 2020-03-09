# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import nested_admin

from abc import ABCMeta

from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db.models import (
    Field
)
from django.db.models.functions import Lower
from django.forms import (
    ModelForm,
    ModelChoiceField,
    ModelMultipleChoiceField,
)
from django_select2.forms import (
    Select2MultipleWidget,
    Select2Widget,
)
from markdownx.fields import MarkdownxFormField

from core_types.admin import PUBLISHABLE_READONLY_FIELDS, ChoiceAdmin
from core_types.models import City
from judges.models import (
    CourtAndBranch,
    Judge,
)
from prisons.models import (
    Prison
)
from prisoners.models import (
    DomesticLawViolated,
    InternationalLawViolated,
)
from report.models import (
    ReportSentence,
    ReportSource,
    ReportQuote,
    ReportComment,
    ReportDetention,
    Report,
    ReportFile,
    HumanRightViolated,
    ReportSentenceBehaviour
)
from types import LambdaType

logger = logging.getLogger(__name__)

publishable_mixin_metadata_fieldset = (
    'Metadata',
    {
        'fields': (
            (
                'is_published',
                'created',
                'updated',
                'created_by',
                'updated_by',
            ),
        ),
        'classes': (
            'ipaFieldset',
            'columns5'
        ),
    },
)


class Select2SingleChoiceField(ModelChoiceField):
    widget = Select2Widget


class Select2MultipleChoiceField(ModelMultipleChoiceField):
    widget = Select2MultipleWidget


def get_select2_field(**kwargs):
    label_from_instance = kwargs.get('label_from_instance', None)
    model = kwargs.get('model', None)
    order_by_attribute = kwargs.get('order_by_attribute', None)
    should_be_multiple_choice = kwargs.get('should_be_multiple_choice', False)

    if should_be_multiple_choice:
        base_class = Select2MultipleChoiceField
    else:
        base_class = Select2SingleChoiceField

    class Select2ChoiceField(base_class):
        __metaclass__ = ABCMeta

        def __init__(
            self,
            **kwargs
        ):
            label_from_instance = kwargs.get('label_from_instance', None)
            model = kwargs.get('model', None)
            order_by_attribute = kwargs.get('order_by_attribute', None)

            queryset = model.objects

            try:
                if isinstance(
                    model._meta.get_field('is_published'),
                    Field
                ):
                    queryset = queryset.filter(is_published=True)
            except FieldDoesNotExist:
                pass

            if type(order_by_attribute) == basestring:
                queryset = queryset.order_by(
                    Lower(order_by_attribute)
                )

            if isinstance(label_from_instance, LambdaType):
                self.label_from_instance = label_from_instance

            super(Select2ChoiceField, self).__init__(
                queryset=queryset
            )

    return Select2ChoiceField(
        label_from_instance=label_from_instance,
        model=model,
        order_by_attribute=order_by_attribute
    )


class ReportSentenceBehaviourInline(nested_admin.NestedStackedInline):
    model = ReportSentenceBehaviour
    max_num = 5
    extra = 0
    readonly_fields = PUBLISHABLE_READONLY_FIELDS
    is_sortable = False

    classes = ('ipaInline', 'fieldsetInlineRelatedItemsCollapsible',)

    fieldsets = (
        publishable_mixin_metadata_fieldset,
        (
            'Judge behaviour',
            {
                'fields': (
                    (
                        'judge_behaviour',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns1',
                ),
            }
        ),
        (
            'Description',
            {
                'fields': (
                    (
                        'description_en',
                        'description_fa',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2',
                ),
            }
        ),
    )


class ReportSentenceAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ReportSentenceBehaviourInline,
    ]

    model = ReportSentence
    list_display = ['__unicode__', 'execution', 'flogging', 'amputation', 'is_published']
    list_editable = ['is_published', 'execution', 'flogging', 'amputation']
    readonly_fields = PUBLISHABLE_READONLY_FIELDS


class ReportSentenceInline(nested_admin.NestedStackedInline):
    model = ReportSentence
    max_num = 5
    extra = 0
    readonly_fields = PUBLISHABLE_READONLY_FIELDS
    classes = ('ipaInline', 'fieldsetInlineRelatedItemsCollapsible',)
    is_sortable = False

    inlines = [
        ReportSentenceBehaviourInline,
    ]

    @staticmethod
    def judge_label_from_instance(instance):
        if isinstance(instance.forename_en, basestring):
            return u'{forename_en} {surname_en}'.format(
                forename_en=instance.forename_en,
                surname_en=instance.surname_en,
            )
        else:
            return instance.surname_en

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return {
            'judge': get_select2_field(
                label_from_instance=self.judge_label_from_instance,
                model=Judge,
                order_by_attribute='surnamename_en',
                should_be_multiple_choice=False,
            ),
            'judge_court_and_branch': get_select2_field(
                label_from_instance=lambda instance: instance.name_en,
                model=CourtAndBranch,
                order_by_attribute='name_en',
                should_be_multiple_choice=False,
            ),
        }.get(
            db_field.name,
            super(ReportSentenceInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        )

    fieldsets = (
        publishable_mixin_metadata_fieldset,
        (
            'Details',
            {
                'fields': (
                    (
                        'amputation',
                        'execution',
                        'flogging',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns3'
                ),
            }
        ),
        (
            'Judge',
            {
                'fields': (
                    (
                        'judge',
                        'judge_court_and_branch',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2'
                ),
            }
        ),
    )


class ReportSourceInline(nested_admin.NestedStackedInline):
    model = ReportSource
    max_num = 5
    extra = 0
    readonly_fields = PUBLISHABLE_READONLY_FIELDS
    classes = ('ipaInline', 'fieldsetInlineRelatedItemsCollapsible',)
    is_sortable = False

    fieldsets = (
        publishable_mixin_metadata_fieldset,
        (
            'Basic information',
            {
                'fields': (
                    (
                        'name',
                        'link',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2'
                ),
            }
        ),
        (
            'Description',
            {
                'fields': (
                    (
                        'description',
                        # TODO: Move back to “Basic information”
                        'related_fields',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2',
                ),
            }
        ),
    )


class ReportDetentionInline(nested_admin.NestedStackedInline):
    model = ReportDetention
    max_num = 5
    extra = 0
    readonly_fields = PUBLISHABLE_READONLY_FIELDS
    classes = ('ipaInline', 'fieldsetInlineRelatedItemsCollapsible',)
    is_sortable = False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return {
            'prison': get_select2_field(
                label_from_instance=lambda instance: instance.name_en,
                model=Prison,
                order_by_attribute='name_en',
                should_be_multiple_choice=False,
            )
        }.get(
            db_field.name,
            super(ReportDetentionInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        )

    fieldsets = (
        publishable_mixin_metadata_fieldset,
        (
            'Details',
            {
                'fields': (
                    (
                        'prison',
                        'detention_type',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2',
                ),
            }
        ),
        (
            'Detention date',
            {
                'fields': (
                    (
                        'detention_year',
                        'detention_month',
                        'detention_day',
                        'detention_year_fa',
                        'detention_month_fa',
                        'detention_day_fa',
                    ),
                    'detention_is_approx',
                ),
                'classes': (
                    'ipaFieldset',
                    'dateFieldset',
                    'dateFieldsetReportDetention',
                    'columns6',
                ),
            }
        ),
    )


class ReportFileInlineForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportFileInlineForm, self).__init__(*args, **kwargs)

        self.fields['description_en'] = MarkdownxFormField()
        self.fields['description_fa'] = MarkdownxFormField()


class ReportFileInline(nested_admin.NestedStackedInline):
    model = ReportFile
    max_num = 5
    extra = 0
    readonly_fields = PUBLISHABLE_READONLY_FIELDS
    classes = ('ipaInline', 'fieldsetInlineRelatedItemsCollapsible',)
    is_sortable = False

    form = ReportFileInlineForm

    fieldsets = (
        publishable_mixin_metadata_fieldset,
        (
            'Name',
            {
                'fields': (
                    (
                        'name_en',
                        'name_fa',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2',
                ),
            }
        ),
        (
            'Description',
            {
                'fields': (
                    (
                        'description_en',
                        'description_fa',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2',
                ),
            }
        ),
        (
            'File',
            {
                'fields': (
                    (
                        'file',
                        'file_thumb',
                        'file_type',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns3',
                ),
            }
        ),
    )


class ReportCommentInline(nested_admin.NestedStackedInline):
    model = ReportComment
    max_num = 5
    extra = 0
    classes = ('ipaInline', 'fieldsetInlineRelatedItemsCollapsible',)
    readonly_fields = (
        'created',
        'user',
    )
    is_sortable = False

    fieldsets = (
        (
            'Metadata',
            {
                'fields': (
                    (
                        'created',
                        'user',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2'
                ),
            },
        ),
        (
            'Name',
            {
                'fields': (
                    'comment',
                ),
                'classes': (
                    'ipaFieldset',
                    'columns1',
                ),
            }
        ),
    )


class ReportQuoteInline(nested_admin.NestedStackedInline):
    model = ReportQuote
    max_num = 5
    extra = 0
    readonly_fields = PUBLISHABLE_READONLY_FIELDS
    classes = ('ipaInline', 'fieldsetInlineRelatedItemsCollapsible',)
    is_sortable = False

    fieldsets = (
        publishable_mixin_metadata_fieldset,
        (
            'Name',
            {
                'fields': (
                    (
                        'name_en',
                        'name_fa',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2',
                ),
            }
        ),
        (
            'Quote',
            {
                'fields': (
                    (
                        'quote_en',
                        'quote_fa',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2',
                ),
            }
        ),
        (
            'Source',
            {
                'fields': (
                    'source',
                ),
                'classes': (
                    'ipaFieldset',
                    'columns1',
                ),
            }
        ),
    )


class ReportAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ReportSourceInline,
        ReportDetentionInline,
        ReportFileInline,
        ReportQuoteInline,
        ReportSentenceInline,
        ReportCommentInline,
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return {
            'city': get_select2_field(
                label_from_instance=lambda instance: instance.name_en,
                model=City,
                order_by_attribute='name_en',
                should_be_multiple_choice=False,
            )
        }.get(
            db_field.name,
            super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return {
            'domestic_law_violated': get_select2_field(
                label_from_instance=lambda instance: instance.name_en,
                model=DomesticLawViolated,
                order_by_attribute='name_en',
                should_be_multiple_choice=True,
            ),
            'international_law_violated': get_select2_field(
                label_from_instance=lambda instance: instance.name_en,
                model=InternationalLawViolated,
                order_by_attribute='name_en',
                should_be_multiple_choice=True,
            ),
            'human_right_violated': get_select2_field(
                label_from_instance=lambda instance: instance.name_en,
                model=HumanRightViolated,
                order_by_attribute='name_en',
                should_be_multiple_choice=True,
            ),
        }.get(
            db_field.name,
            super(ReportAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        )

    model = Report
    list_display = ['__unicode__', 'is_published']
    list_editable = ['is_published']
    search_fields = ['abstract']
    readonly_fields = PUBLISHABLE_READONLY_FIELDS

    fieldsets = (
        publishable_mixin_metadata_fieldset,
        (
            'Abstract',
            {
                'fields': (
                    (
                        'abstract_text_en',
                        'abstract_text_fa',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns2'
                ),
            }
        ),
        (
            'Details',
            {
                'fields': (
                    (
                        'city',
                        'victim_count',
                        'picture',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns3'
                ),
            }
        ),
        (
            'Violations',
            {
                'fields': (
                    (
                        'domestic_law_violated',
                        'international_law_violated',
                        'human_right_violated',
                    ),
                ),
                'classes': (
                    'ipaFieldset',
                    'columns3',
                ),
            }
        ),
    )

    class Media:
        css = {
            "all": (
                "admin_assets/css/admin.css",
            )
        }
        js = (
            "admin_assets/js/jquery-2.2.4.min.js",
            "admin_assets/js/jalaali-js-1.1.2.js",
            "admin_assets/js/utils.js",
            "admin_assets/js/Admin.js",
            "admin_assets/js/DateFieldset.js",
            "admin_assets/js/InlineFieldset.js",
            "admin_assets/js/InlineFieldsetRelatedItem.js",
            "admin_assets/js/main.js",
        )


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportDetention)
admin.site.register(HumanRightViolated, ChoiceAdmin)
admin.site.register(ReportSentence, ReportSentenceAdmin)
