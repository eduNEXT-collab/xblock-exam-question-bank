"""Mock backend for content libraries for testing purposes."""


class MockComponent:
    """Mock component object."""

    def __init__(self, learning_package_id=None, entity_ref=None):
        self.learning_package_id = learning_package_id or 1
        self.entity_ref = entity_ref or "mock-entity-ref"


def get_component_from_usage_key():
    """Return a mock get_component_from_usage_key function."""
    def mock_get_component_from_usage_key(usage_key):
        """Mock implementation that returns a mock component."""
        return MockComponent(
            learning_package_id=1,
            entity_ref=str(usage_key)
        )
    return mock_get_component_from_usage_key
