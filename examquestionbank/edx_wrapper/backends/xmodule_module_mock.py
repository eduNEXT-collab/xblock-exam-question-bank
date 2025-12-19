"""Mock backend for xmodule for testing purposes."""


def _mock_display_name_with_default(block):
    """Mock display_name_with_default function."""
    return getattr(block, "display_name", "Test Block")


class MockItemBankMixin:
    """Mock ItemBankMixin class for testing."""

    max_count = -1
    children = []
    allow_resetting_children = False

    def get_children(self):
        """Return children blocks."""
        return self.children

    def _get_selected_child_blocks(self):
        """Return selected child blocks."""
        return self.children


MOCK_STUDENT_VIEW = "student_view"


def get_display_name_with_default():
    """Return mock display_name_with_default function."""
    return _mock_display_name_with_default


def get_item_bank_mixin():
    """Return mock ItemBankMixin class."""
    return MockItemBankMixin


def get_student_view():
    """Return mock STUDENT_VIEW constant."""
    return MOCK_STUDENT_VIEW
