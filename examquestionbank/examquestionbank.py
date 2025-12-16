"""
ExamQuestionBankXBlock

An instructor-facing XBlock that extends the Open edX Item Bank logic
to provide a summarized and instructor-friendly authoring experience.

This block allows instructors to:
- Select individual problems from Content Libraries (via ItemBankMixin)
- Configure how many problems will be shown to learners
- View a concise summary of the bank instead of a full problem listing
"""

from web_fragments.fragment import Fragment
from xblock.fields import Scope, String
from xblock.utils.resources import ResourceLoader
from xmodule.item_bank_block import ItemBankMixin
from xblock.core import XBlock

resource_loader = ResourceLoader(__name__)

_ = lambda text: text


class ExamQuestionBankXBlock(ItemBankMixin, XBlock):
    """
    Custom Item Bank XBlock for exams.

    This XBlock reuses the core ItemBankBlock behavior for selecting
    problems from Content Libraries, while customizing the Studio
    authoring experience to display a high-level summary.
    """

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        default="Exam Question Bank",
        scope=Scope.settings,
    )

    @classmethod
    def get_selected_event_prefix(cls) -> str:
        """
        Event prefix used by ExamQuestionBankXBlock when emitting selection events.
        """
        return "edx.examquestionbank.content"

    def author_view(self, context=None):
        """
        Studio author view.

        - When the block is opened in 'View' mode, render the real children
          so instructors can preview and manage selected problems.
        - Otherwise, render a custom summary view plus the 'Add Problems'
          action.
        """
        fragment = Fragment()

        self._add_css(fragment)

        if self._is_root_with_children(context):
            self._render_children_view(context, fragment)
        else:
            self._render_summary_view(fragment)
            self._render_add_view(fragment)

        return fragment

    def _add_css(self, fragment: Fragment) -> None:
        """Attach XBlock-specific CSS."""
        css = resource_loader.load_unicode("static/css/examquestionbank.css")
        fragment.add_css(css)

    def _is_root_with_children(self, context) -> bool:
        """
        Return True if this block is the root being viewed in Studio
        and it has selected child blocks.
        """
        if not context:
            return False

        root_xblock = context.get("root_xblock")
        return bool(root_xblock and root_xblock.usage_key == self.usage_key and self.children)

    def _render_children_view(self, context, fragment: Fragment) -> None:
        """
        Render the actual child blocks.
        """
        context["can_edit_visibility"] = False
        context["can_move"] = False
        context["can_collapse"] = True

        self.render_children(
            context,
            fragment,
            can_reorder=False,
            can_add=False,
        )

    def _render_summary_view(self, fragment: Fragment) -> None:
        """
        Render the summarized author view showing bank size
        and configuration state.
        """
        summary_html = resource_loader.render_django_template(
            "templates/item_bank/author_view_custom.html",
            {
                "block_count": len(self.children),
                "max_count": self.max_count,
                "view_link": f'<a target="_top" href="/container/{self.usage_key}">',
            },
        )
        fragment.add_content(summary_html)

    def _render_add_view(self, fragment: Fragment) -> None:
        """
        Render the 'Add Problems' action view.
        """
        add_html = resource_loader.render_django_template(
            "templates/item_bank/author_view_add_custom.html",
            {}
        )
        fragment.add_content(add_html)
