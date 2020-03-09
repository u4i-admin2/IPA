# coding: utf-8

import logging

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render
from django.views.generic import View
from public.utils import (
    get_styles,
    get_view_context_with_defaults,
)


logger = logging.getLogger(__name__)


class Home(View):
    def get(self, request, *args, **kwargs):
        head_image = (
            static('public/img/og_Intro_Screen_FB_2.png') + '?v=2019-08-28'
        )

        return render(
            request,
            'home.html',
            context=get_view_context_with_defaults(
                {
                    'head_image': head_image,
                    'styles': get_styles('home'),
                },
                request,
            ),
        )
