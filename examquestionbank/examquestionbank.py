"""
ExamQuestionBankXBlock - Custom Item Bank for exams.

Extends Open edX ItemBankMixin to provide a custom Studio authoring experience.
"""
import logging
from copy import copy

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.utils.resources import ResourceLoader
from xmodule.item_bank_block import ItemBankMixin
from xmodule.x_module import STUDENT_VIEW

resource_loader = ResourceLoader(__name__)
logger = logging.getLogger(__name__)
_ = lambda text: text


class ExamQuestionBankXBlock(ItemBankMixin, XBlock):
    """Custom Item Bank XBlock for exams."""

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        default="Exam Question Bank",
        scope=Scope.settings,
    )

    @classmethod
    def get_selected_event_prefix(cls) -> str:
        """Event prefix for selection events."""
        return "edx.examquestionbank.content"

    def author_view(self, context=None):
        """Studio author view."""
        fragment = Fragment()
        fragment.add_css(resource_loader.load_unicode("static/css/examquestionbank.css"))

        root_xblock = context.get("root_xblock") if context else None
        is_root = root_xblock and root_xblock.usage_key == self.usage_key

        if is_root and self.children:
            context["can_edit_visibility"] = False
            context["can_move"] = False
            context["can_collapse"] = True
            self.render_children(context, fragment, can_reorder=False, can_add=False)
        else:
            fragment.add_content(resource_loader.render_django_template(
                "templates/item_bank/author_view_custom.html",
                {
                    "block_count": len(self.children),
                    "max_count": self.max_count,
                    "view_link": f'<a target="_top" href="/container/{self.usage_key}">',
                },
            ))
            fragment.add_content(resource_loader.render_django_template(
                "templates/item_bank/author_view_add_custom.html", {}
            ))

        return fragment

    def student_view(self, context):
        """LMS student view."""
        fragment = Fragment()
        contents = []
        child_context = copy(context) if context else {}

        for child in self._get_selected_child_blocks():
            if child is None:
                logger.error("Skipping display for child block that is None")
                continue
            rendered_child = child.render(STUDENT_VIEW, child_context)
            fragment.add_fragment_resources(rendered_child)
            contents.append({"id": str(child.usage_key), "content": rendered_child.content})

        fragment.add_content(
            self.runtime.service(self, "mako").render_lms_template(
                "vert_module.html",
                {
                    "items": contents,
                    "xblock_context": context,
                    "show_bookmark_button": False,
                    "watched_completable_blocks": set(),
                    "completion_delay_ms": None,
                    "reset_button": self.allow_resetting_children,
                },
            )
        )
        return fragment

    def format_block_keys_for_analytics(self, block_keys):
        """Format block keys for analytics events."""
        return [
            {"usage_key": str(self.context_key.make_usage_key(*block_key))}
            for block_key in block_keys
        ]
