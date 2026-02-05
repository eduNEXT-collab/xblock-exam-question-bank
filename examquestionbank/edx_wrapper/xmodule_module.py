"""Xmodule definitions (wrapper around edx-platform)."""

from importlib import import_module

from django.conf import settings


def _backend():
    """Return the backend module for xmodule operations."""
    path = getattr(
        settings,
        "EXAMQUESTIONBANK_XMODULE_BACKEND",
        "examquestionbank.edx_wrapper.backends.xmodule_module_v1",
    )
    return import_module(path)


def get_display_name_with_default():
    """Return the display_name_with_default function from the backend."""
    return _backend().get_display_name_with_default()


def get_item_bank_mixin():
    """Return the ItemBankMixin class from the backend."""
    return _backend().get_item_bank_mixin()


def get_student_view():
    """Return the STUDENT_VIEW constant from the backend."""
    return _backend().get_student_view()

def get_modulestore():
    """Return the modulestore instance from the backend."""
    return _backend().get_modulestore()
