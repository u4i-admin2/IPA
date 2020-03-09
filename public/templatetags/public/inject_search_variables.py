# coding: utf-8

import json

from django.utils.safestring import mark_safe

import prisoners.models
import judges.models
import prisons.models


def inject_search_variables(context):
    search = {}
    search['judges'] = {x.id: x.get_name() for x in judges.models.Judge.published_objects.all()}
    search['prisons'] = {x.id: x.name for x in prisons.models.Prison.published_objects.all()}

    if context.request.ipa_site == 'ipa':
        search['prisoners'] = {x.id: x.get_name() for x in prisoners.models.Prisoner.published_objects.all()}

    return mark_safe(json.dumps(search))
