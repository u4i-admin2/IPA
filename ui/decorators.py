"""
Wrap some Django decorators to change their defaults for our UI customizations.
"""

from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
import django.contrib.auth.decorators


def login_required(*args, **kwargs):
    """
    Wrap django.contrib.auth.decorators.login_required().
    """
    kwargs['login_url'] = reverse_lazy('ui:users:login')
    return django.contrib.auth.decorators.login_required(*args, **kwargs)


def class_login_required(cls):
    """
    Class decorator that applies @login_required to the class even if it
    overrides its dispatch() method.
    """
    decorator = method_decorator(login_required)
    cls.dispatch = decorator(cls.dispatch)
    return cls
