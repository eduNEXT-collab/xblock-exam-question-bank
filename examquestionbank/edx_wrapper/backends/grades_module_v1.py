"""Backend abstraction for grades from edx-platform."""

# pylint: disable=import-error
from lms.djangoapps.grades.scores import compute_percent


def get_compute_percent():
    """Return compute_percent function."""
    return compute_percent
