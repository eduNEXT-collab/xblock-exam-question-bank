"""
ExamQuestionBankXBlock - Custom Item Bank for exams.

Extends Open edX ItemBankMixin to provide a custom Studio authoring experience.
"""
import logging
from copy import copy

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Boolean, Float, Integer, List, Scope, String
from xblock.utils.resources import ResourceLoader

from examquestionbank.edx_wrapper.grades_module import get_course_data, get_subsection_grade_factory
from examquestionbank.edx_wrapper.xmodule_module import (
    get_display_name_with_default,
    get_item_bank_mixin,
    get_student_view,
)

resource_loader = ResourceLoader(__name__)
logger = logging.getLogger(__name__)

display_name_with_default = get_display_name_with_default()
ItemBankMixin = get_item_bank_mixin()
STUDENT_VIEW = get_student_view()
SubsectionGradeFactory = get_subsection_grade_factory()
CourseData = get_course_data()


def _(text):
    return text


class ExamQuestionBankXBlock(ItemBankMixin, XBlock):
    """Custom Item Bank XBlock for exams."""

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        default="Exam Question Bank",
        scope=Scope.settings,
    )

    max_exam_attempts = Integer(
        display_name=_("Maximum Exam Attempts"),
        help=_(
            "Maximum number of times a student can attempt this entire exam. "
            "Set to -1 for unlimited attempts."
        ),
        default=3,
        scope=Scope.settings,
        values={"min": -1},
    )

    current_attempt = Integer(
        display_name="Current Attempt",
        help="Current attempt number for this student",
        default=1,
        scope=Scope.user_state
    )

    attempt_history = List(
        display_name="Attempt History",
        help="History of all attempts with scores and timestamps",
        default=[],
        scope=Scope.user_state
    )

    minimum_passing_score = Float(
        display_name="Minimum Passing Score (%)",
        help="Minimum percentage required to pass the exam (1-100)",
        default=60.0,
        scope=Scope.settings,
        values={"min": 1, "max": 100}
    )

    is_attempting = Boolean(
        display_name="Is Attempting",
        help="Indicates whether the student is currently attempting the exam",
        default=True,
        scope=Scope.user_state
    )

    @classmethod
    def get_selected_event_prefix(cls) -> str:
        """Event prefix for selection events."""
        return "edx.examquestionbank.content"

    def author_view(self, context=None):
        """Studio author view."""
        fragment = Fragment()
        fragment.add_css(resource_loader.load_unicode("static/css/author_view.css"))

        root_xblock = context.get("root_xblock") if context else None
        is_root = root_xblock and root_xblock.usage_key == self.usage_key

        if is_root and self.children:
            context["can_edit_visibility"] = False
            context["can_move"] = False
            context["can_collapse"] = True
            self.render_children(context, fragment, can_reorder=False, can_add=False)
        else:
            fragment.add_content(resource_loader.render_django_template(
                "templates/author_view_custom.html",
                {
                    "block_count": len(self.children),
                    "max_count": self.max_count,
                    "blocks": [
                        {"display_name": display_name_with_default(child)}
                        for child in self.get_children()
                    ],
                    "view_link": f'<a target="_top" href="/container/{self.usage_key}">',
                },
            ))
            fragment.add_content(resource_loader.render_django_template(
                "templates/author_view_add_custom.html", {}
            ))

        return fragment

    def student_view(self, context):
        """LMS student view."""
        fragment = Fragment()
        fragment.add_css(resource_loader.load_unicode("static/css/student_view.css"))
        fragment.add_javascript(resource_loader.load_unicode("static/js/student_view.js"))
        contents = []

        context = copy(context) if context else {}

        # Attempt information
        context['current_attempt'] = self.current_attempt
        context['max_attempts'] = self.max_exam_attempts

        # Exam status
        current_grade = self.get_current_grade()
        context['can_retry'] = self.can_retry(current_grade=current_grade)
        context['can_submit'] = self.can_submit(current_grade=current_grade)
        context['current_grade'] = current_grade
        context['minimum_passing_score'] = self.minimum_passing_score
        context['is_attempting'] = self.is_attempting

        child_context = copy(context)

        for child in self._get_selected_child_blocks():
            if child is None:
                logger.error("Skipping display for child block that is None")
                continue
            rendered_child = child.render(STUDENT_VIEW, child_context)
            fragment.add_fragment_resources(rendered_child)
            contents.append({"id": str(child.usage_key), "content": rendered_child.content})

        fragment.add_content(
            resource_loader.render_django_template(
                "templates/student_view_vert_mod.html",
                {
                    "items": contents,
                    'show_bookmark_button': False,
                    'watched_completable_blocks': set(),
                    'completion_delay_ms': None,
                    **context,
                },
            )
        )
        fragment.initialize_js('ExamQuestionBankBlock')
        return fragment

    def format_block_keys_for_analytics(self, block_keys):
        """Format block keys for analytics events."""
        return [
            {"usage_key": str(self.context_key.make_usage_key(*block_key))}
            for block_key in block_keys
        ]

    @XBlock.json_handler
    def submit_exam(self, _, __):
        """
        Validate and finalize exam submission.

        Updates attempt count and marks exam as not attempting.
        """
        # Check if can submit (must be currently attempting and have attempts left)
        if not self.is_attempting:
            return {
                'success': False,
                'error': 'Not currently attempting exam.'
            }

        if self.max_exam_attempts > -1 and self.current_attempt > self.max_exam_attempts:
            return {
                'success': False,
                'error': 'No attempts remaining.'
            }

        # Update state
        self.current_attempt += 1
        self.is_attempting = False

        return {'success': True}

    @XBlock.json_handler
    def retry_exam(self, _, __):
        """
        Allow the student to retry the exam by resetting problems.
        """
        # Validate that the student can attempt again
        current_grade = self.get_current_grade()
        if not self.can_retry(current_grade=current_grade):
            return {
                'success': False,
                'error': 'No attempts remaining or conditions not met for retry.'
            }

        for block_type, block_id in self.selected_children():
            block = self.runtime.get_block(self.context_key.make_usage_key(block_type, block_id))
            if hasattr(block, 'reset_problem'):
                block.reset_problem(None)
                block.save()

        self.selected = []  # pylint: disable=attribute-defined-outside-init
        self.is_attempting = True

        return {'success': True}

    def can_retry(self, current_grade):
        """
        Check if the student can retry the exam.
        """
        if current_grade >= self.minimum_passing_score:
            return False

        if self.is_attempting:
            return False

        if self.max_exam_attempts == -1:
            return True

        if self.current_attempt <= self.max_exam_attempts:
            return True

        return False

    def can_submit(self, current_grade):
        """
        Check if the student can attempt the exam again.

        Returns True if attempts are unlimited or current attempts are less than max attempts.
        """
        if current_grade >= self.minimum_passing_score:
            return False

        if self.max_exam_attempts > -1 and self.current_attempt > self.max_exam_attempts:
            return False

        return self.is_attempting

    def get_current_grade(self):
        """
        Return the current grade for the exam as a percentage (0-100).
        """
        try:
            subsection_block = self.get_parent().get_parent()
            subsection_key = subsection_block.usage_key
            student = self.runtime.get_real_user(self.runtime.anonymous_student_id)

            course_data = CourseData(user=student, course_key=subsection_key.course_key)
            grade_factory = SubsectionGradeFactory(student, course_data=course_data)
            subsection_grade = grade_factory.create(subsection_block)
            percent_graded = subsection_grade.percent_graded * 100
            return percent_graded

        except Exception as e:
            raise RuntimeError("Error retrieving current grade") from e
