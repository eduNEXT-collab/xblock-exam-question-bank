"""
Settings for the Exam Question Bank plugin.
"""


def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """
    settings.EXAMQUESTIONBANK_XMODULE_BACKEND = 'examquestionbank.edx_wrapper.backends.xmodule_module_v1'
    settings.EXAMQUESTIONBANK_GRADES_BACKEND = 'examquestionbank.edx_wrapper.backends.grades_module_v1'
