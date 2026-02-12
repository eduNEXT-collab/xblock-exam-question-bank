"""
Settings for the plugin.
"""


def plugin_settings(settings):
    """
    Read / Update necessary project settings for production envs.
    """
    settings.EXAMQUESTIONBANK_XMODULE_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "EXAMQUESTIONBANK_XMODULE_BACKEND",
        settings.EXAMQUESTIONBANK_XMODULE_BACKEND
    )
    settings.EXAMQUESTIONBANK_CONTENT_LIBRARIES_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "EXAMQUESTIONBANK_CONTENT_LIBRARIES_BACKEND",
        settings.EXAMQUESTIONBANK_CONTENT_LIBRARIES_BACKEND
    )
