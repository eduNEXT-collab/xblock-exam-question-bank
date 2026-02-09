"""Backend abstraction for content libraries from edx-platform."""

# pylint: disable=import-error
from openedx.core.djangoapps.content_libraries.api import get_component_from_usage_key


def get_component_from_usage_key():     # pylint: disable=function-redefined
    """Return get_component_from_usage_key function."""
    return get_component_from_usage_key
