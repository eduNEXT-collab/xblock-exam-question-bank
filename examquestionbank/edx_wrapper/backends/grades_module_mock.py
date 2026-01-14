"""Mock backend for grades for testing purposes."""


def get_compute_percent():
    """Return a mock compute_percent function."""
    def compute_percent_mock(earned, possible):
        if possible == 0:
            return 0.0
        return (earned / possible) * 100.0
    return compute_percent_mock
