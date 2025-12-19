"""Pytest configuration for examquestionbank tests."""

import os
import django
from django.conf import settings


def pytest_configure():
    """Configure Django settings before running tests."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'examquestionbank.settings.test')
    
    if not settings.configured:
        django.setup()
