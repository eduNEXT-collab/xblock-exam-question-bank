"""
Settings for the Exam Question Bank plugin.
"""


def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """
    settings.EXAMQUESTIONBANK_XMODULE_BACKEND = 'examquestionbank.edx_wrapper.backends.xmodule_module_v1'
    settings.EXAMQUESTIONBANK_GRADES_BACKEND = 'examquestionbank.edx_wrapper.backends.grades_module_v1'

    import os
    try:
        # __file__ is examquestionbank/settings/common.py
        # We need to go up to examquestionbank/ root
        settings_dir = os.path.dirname(os.path.abspath(__file__))  # examquestionbank/settings/
        package_dir = os.path.dirname(settings_dir)  # examquestionbank/
        
        # Try both possible locations
        for subdir in ['translations', 'conf/locale']:
            locale_path = os.path.join(package_dir, subdir)
            if os.path.exists(locale_path):
                if not hasattr(settings, 'LOCALE_PATHS'):
                    settings.LOCALE_PATHS = []
                
                locale_paths = list(settings.LOCALE_PATHS)
                if locale_path not in locale_paths:
                    locale_paths.append(locale_path)
                    settings.LOCALE_PATHS = locale_paths
                break
    except Exception:
        # Don't break Django startup if this fails
        pass