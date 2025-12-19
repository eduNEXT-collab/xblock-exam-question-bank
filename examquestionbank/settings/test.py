"""Test settings for examquestionbank XBlock."""

SECRET_KEY = 'test-secret-key'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.db',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'examquestionbank',
]

EXAMQUESTIONBANK_XMODULE_BACKEND = 'examquestionbank.edx_wrapper.backends.xmodule_module_mock'
