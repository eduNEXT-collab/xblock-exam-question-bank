"""Grades definitions (wrapper around edx-platform)."""

from importlib import import_module

from django.conf import settings


def _backend():
    """Return the backend module for grades operations."""
    path = getattr(
        settings,
        "EXAMQUESTIONBANK_GRADES_BACKEND",
        "examquestionbank.edx_wrapper.backends.grades_module_v1",
    )
    return import_module(path)


def get_subsection_grade_factory():
    """Return the SubsectionGradeFactory class from the backend."""
    return _backend().get_subsection_grade_factory()


def get_course_data():
    """Return the CourseData class from the backend."""
    return _backend().get_course_data()
