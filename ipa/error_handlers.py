# coding: utf-8

from public.views_v2 import Error


def handler400(request, *args, **argv):
    return Error.as_view()(
        request,
        status=400,
    )


def handler403(request, *args, **argv):
    return Error.as_view()(
        request,
        status=403,
    )


def handler404(request, *args, **argv):
    return Error.as_view()(
        request,
        status=404,
    )


def handler500(request, *args, **argv):
    return Error.as_view()(
        request,
        status=500,
    )
