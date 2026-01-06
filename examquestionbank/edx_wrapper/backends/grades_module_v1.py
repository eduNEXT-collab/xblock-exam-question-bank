"""Backend abstraction for grades from edx-platform."""

# pylint: disable=import-error
from lms.djangoapps.grades.api import SubsectionGradeFactory
from lms.djangoapps.grades.course_data import CourseData


def get_subsection_grade_factory():
    """Return SubsectionGradeFactory class."""
    return SubsectionGradeFactory


def get_course_data():
    """Return CourseData class."""
    return CourseData
