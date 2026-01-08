"""Backend abstraction for grades from edx-platform."""

# pylint: disable=import-error
from lms.djangoapps.grades.api import SubsectionGradeFactory
from lms.djangoapps.grades.course_data import CourseData
from lms.djangoapps.grades.scores import compute_percent


def get_subsection_grade_factory():
    """Return SubsectionGradeFactory class."""
    return SubsectionGradeFactory


def get_course_data():
    """Return CourseData class."""
    return CourseData


def get_compute_percent():
    """Return compute_percent function."""
    return compute_percent
