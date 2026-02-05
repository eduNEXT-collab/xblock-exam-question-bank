"""Content Libraries definitions (wrapper around edx-platform)."""

from importlib import import_module

from django.conf import settings


def _backend():
    """Return the backend module for content libraries operations."""
    path = getattr(
        settings,
        "EXAMQUESTIONBANK_CONTENT_LIBRARIES_BACKEND",
        "examquestionbank.edx_wrapper.backends.content_libraries_module_v1",
    )
    return import_module(path)


def get_component_from_usage_key():
    """Return the get_component_from_usage_key function from the backend."""
    return _backend().get_component_from_usage_key()
