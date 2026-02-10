"""Backend abstraction for xmodule from edx-platform."""

# pylint: disable=import-error
from xmodule.block_metadata_utils import display_name_with_default
from xmodule.item_bank_block import ItemBankMixin
from xmodule.x_module import STUDENT_VIEW


def get_display_name_with_default():
    """Return display_name_with_default function."""
    return display_name_with_default


def get_item_bank_mixin():
    """Return ItemBankMixin class."""
    return ItemBankMixin


def get_student_view():
    """Return STUDENT_VIEW constant."""
    return STUDENT_VIEW


def get_modulestore():
    """Return modulestore instance."""
    # Lazy import to avoid circular import issues
    from xmodule.modulestore.django import modulestore  # pylint: disable=import-outside-toplevel
    return modulestore()
