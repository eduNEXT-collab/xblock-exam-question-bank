"""
ExamQuestionBankXBlock - Custom Item Bank for exams.

Extends Open edX ItemBankMixin to provide a custom Studio authoring experience.
"""
import logging
import random
from copy import copy
from importlib import resources

from django.utils import translation
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Boolean, Dict, Float, Integer, List, Scope, String
from xblock.utils.resources import ResourceLoader

from examquestionbank.edx_wrapper.content_libraries_module import get_component_from_usage_key
from examquestionbank.edx_wrapper.grades_module import get_compute_percent
from examquestionbank.edx_wrapper.xmodule_module import (
    get_display_name_with_default,
    get_item_bank_mixin,
    get_modulestore,
    get_student_view,
)

resource_loader = ResourceLoader(__name__)
logger = logging.getLogger(__name__)

display_name_with_default = get_display_name_with_default()
ItemBankMixin = get_item_bank_mixin()
STUDENT_VIEW = get_student_view()
compute_percent = get_compute_percent()
get_component_from_usage_key_func = get_component_from_usage_key()


def _(text):
    return text


@XBlock.needs("i18n")
class ExamQuestionBankXBlock(ItemBankMixin, XBlock):
    """Custom Item Bank XBlock for exams."""

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        default="Exam Question Bank",
        scope=Scope.settings,
    )

    # Override parent field to set translation
    max_count = Integer(
        display_name=_("Count"),
        help=_("Enter the number of components to display to each student. Set it to -1 to display all components."),
        default=-1,
        scope=Scope.settings,
    )

    max_count_per_collection = Dict(
        display_name=_("Max Count Per Collection"),
        help=_("Optional limit on the number of problems to display from each collection. Set to -1 for no limit."),
        default={},
        scope=Scope.settings,
    )

    collections_info = Dict(
        display_name=_("Collections Info"),
        help=_("To update this field click Refresh Collections in the XBlock."),
        default={},
        scope=Scope.content,
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
        display_name=_("Current Attempt"),
        help=_("Current attempt number for this student"),
        default=1,
        scope=Scope.user_state
    )

    attempt_history = List(
        display_name=_("Attempt History"),
        help=_("History of all attempts with scores and timestamps"),
        default=[],
        scope=Scope.user_state
    )

    minimum_passing_score = Float(
        display_name=_("Minimum Passing Score (%)"),
        help=_("Minimum percentage required to pass the exam (1-100)"),
        default=60.0,
        scope=Scope.settings,
        values={"min": 1, "max": 100}
    )

    is_attempting = Boolean(
        display_name=_("Is Attempting"),
        help=_("Indicates whether the student is currently attempting the exam"),
        default=True,
        scope=Scope.user_state
    )

    # Override parent field to hide it from editor
    allow_resetting_children = Boolean(
        default=False,
        scope=Scope.user_state,
        enforce_type=True
    )

    @staticmethod
    def _get_statici18n_js_url(loader):  # pragma: no cover
        """
        Return the JavaScript translation file for the current language.

        Uses importlib.resources to locate the static i18n file.
        """
        lang_code = translation.get_language()
        if not lang_code:
            return None
        text_js = 'public/js/translations/{lang_code}/text.js'
        country_code = lang_code.split('-')[0]
        for code in (translation.to_locale(lang_code), lang_code, country_code):
            try:
                # Check if the resource exists using importlib.resources
                if resources.files(loader.module_name).joinpath(text_js.format(lang_code=code)).is_file():
                    return text_js.format(lang_code=code)
            except (TypeError, AttributeError, FileNotFoundError):
                continue
        return None

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

        collections_with_values = {}

        for coll_key, coll_data in self.collections_info.items():
            collections_with_values[coll_key] = {
                **coll_data,  # keep title, description, problems
                "current_value": self.max_count_per_collection.get(coll_key, 1)
            }

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
                    "collection_group": collections_with_values,
                },
                i18n_service=self.runtime.service(self, 'i18n')
            ))
            fragment.add_content(resource_loader.render_django_template(
                "templates/author_view_add_custom.html", {}, i18n_service=self.runtime.service(self, 'i18n')
            ))
            fragment.add_javascript(resource_loader.load_unicode("static/js/author_view.js"))
            statici18n_js_url = self._get_statici18n_js_url(resource_loader)
            if statici18n_js_url:
                fragment.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))
            fragment.initialize_js('ExamQuestionBankAuthorView')

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
                    **context,
                },
                i18n_service=self.runtime.service(self, 'i18n')
            )
        )
        statici18n_js_url = self._get_statici18n_js_url(resource_loader)
        if statici18n_js_url:
            fragment.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))
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
        self.current_attempt += 1
        self.is_attempting = True

        return {'success': True}

    def can_retry(self, current_grade):
        """
        Check if the student should see the retry button.
        """
        if current_grade >= self.minimum_passing_score or self.is_attempting:
            return False

        has_attempts_left = (self.max_exam_attempts == -1) or \
                            (self.current_attempt < self.max_exam_attempts)

        return has_attempts_left

    def can_submit(self, current_grade):
        """
        Check if the student can see the submit exam button.

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

        Calculates grade directly from selected problems without using grade factory.
        This manually replicates the weighted score aggregation logic.
        """
        total_weighted_earned = 0.0
        total_weighted_possible = 0.0

        # Iterate through selected problems
        for block_type, block_id in self.selected_children():
            block_usage_key = self.context_key.make_usage_key(block_type, block_id)
            block = self.runtime.get_block(block_usage_key)

            # Only process blocks that have scores
            if not getattr(block, 'has_score', False):
                continue

            # Get the score from the block
            score_tuple = block.get_score()
            if score_tuple is None:
                # Problem not attempted, treat as 0 earned
                raw_earned = 0.0
                raw_possible = block.max_score() or 0.0
            else:
                raw_earned, raw_possible = score_tuple

            # Get weight from the block (if it exists)
            weight = getattr(block, 'weight', None)

            # Calculate weighted scores
            if weight is not None and raw_possible > 0:
                # Apply weight: weighted_earned = (raw_earned / raw_possible) * weight
                weighted_earned = raw_earned * weight / raw_possible
                weighted_possible = float(weight)
            else:
                # No weight, use raw scores
                weighted_earned = raw_earned
                weighted_possible = raw_possible

            total_weighted_earned += weighted_earned
            total_weighted_possible += weighted_possible

        # Calculate percentage using compute_percent
        percent_graded = compute_percent(total_weighted_earned, total_weighted_possible) * 100
        return percent_graded

    def populate_collections_info_from_children(self):
        """
        Populate collections_info with grouped collection data.

        Fetch children block information and group them by their collections.
        """
        # Import here to avoid Django setup issues during module import
        from opaque_keys.edx.keys import UsageKey  # pylint: disable=import-outside-toplevel
        from openedx_learning.api import authoring as authoring_api  # pylint: disable=import-outside-toplevel

        # Temporary storage for children data
        children_data = {}
        modulestore = get_modulestore()

        for child in self.children:
            block = modulestore.get_item(child)
            if hasattr(block, 'upstream'):
                key_string = block.upstream
                # Get the Component from the usage key
                usage_key = UsageKey.from_string(key_string)
                component = get_component_from_usage_key_func(usage_key)

                # Get collections for this component
                collections = authoring_api.get_entity_collections(
                    component.learning_package_id,
                    component.key,
                )
                # Convert collection objects to serializable dictionaries
                serialized_collections = [
                    {
                        "key": coll.key,
                        "title": coll.title,
                        "description": getattr(coll, 'description', '')
                    }
                    for coll in collections
                ]
                children_data[str(child)] = {
                    "display_name": display_name_with_default(block),
                    "library_usage_key": str(usage_key),
                    "collections": serialized_collections,
                }

        # Group the data by collections
        grouped_data = {}

        for block_key, info in children_data.items():
            collections = info.get('collections', [])
            display_name = info.get('display_name', 'Unknown')
            library_key = info.get('library_usage_key', '')

            # If there are no collections, group under 'uncategorized'
            if not collections:
                if "uncategorized" not in grouped_data:
                    grouped_data["uncategorized"] = {
                        "title": "Uncategorized",
                        "description": "Problems without a collection",
                        "problems": {}
                    }

                grouped_data["uncategorized"]["problems"][block_key] = {
                    "name": display_name,
                    "library_key": library_key
                }
                continue

            for collection in collections:
                coll_key = collection['key']

                if coll_key not in grouped_data:
                    grouped_data[coll_key] = {
                        "title": collection['title'],
                        "description": collection.get('description', ''),
                        "problems": {}
                    }

                grouped_data[coll_key]["problems"][block_key] = {
                    "name": display_name,
                    "library_key": library_key
                }
        return grouped_data

    @XBlock.json_handler
    def refresh_collections(self, _, __):
        """
        Refresh collections_info.

        Populate collection data from children and save automatically.
        """
        if not self.children:
            return {
                'success': False,
                'message': 'No problems found to process'
            }

        try:
            grouped_data = self.populate_collections_info_from_children()
            self.collections_info = grouped_data

            # Use modulestore to persist changes
            modulestore = get_modulestore()
            modulestore.update_item(self, self.runtime.user_id)

            return {
                'success': True,
                'message': 'Collections refreshed!',
                'collections_info': grouped_data
            }
        except Exception as e:      # pylint: disable=broad-exception-caught
            logger.exception(f"Error: {str(e)}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }

    @classmethod
    def make_selection(
        cls,
        selected,
        children,
        max_count,
        max_count_per_collection=None,
        collections_info=None
    ):  # pylint: disable=too-many-positional-arguments
        """
        Make a selection based on max_count and max_count_per_collection if provided, if not use the old logic.

        Returns a dictionary with keys:
        - 'selected': set of (block_type, block_id) tuples that should be selected for display
        - 'invalid': sorted list of (block_type, block_id) tuples that were in the original
           selected set but are no longer valid (e.g. because the child blocks changed)
        - 'overlimit': sorted list of (block_type, block_id) tuples that were in the original
           selected set but exceed the max_count limit
        - 'added': sorted list of (block_type, block_id) tuples that were not in the original
           selected set but are now selected based on the new criteria.
        """
        # New logic for selecting children by collection.
        if max_count_per_collection and collections_info:
            rand = random.Random()
            selected_keys = {tuple(k) for k in selected}  # set of (block_type, block_id)

            # Determine which of our children we will show:
            # The block_keys format is (block_type, block_id).
            valid_block_keys = {(c.block_type, c.block_id) for c in children}

            # Remove any selected blocks that are no longer valid:
            invalid_block_keys = selected_keys - valid_block_keys
            if invalid_block_keys:
                selected_keys -= invalid_block_keys

            # Build a mapping from usage key string to (block_type, block_id)
            usage_key_to_block_key = {}
            for child in children:
                usage_key_str = str(child)
                usage_key_to_block_key[usage_key_str] = (child.block_type, child.block_id)

            # Track selected problems per collection
            new_selected_keys = set()
            used_problems = set()  # Track problems already selected to avoid duplicates

            for collection_key, count_str in max_count_per_collection.items():
                count = int(count_str)

                if collection_key not in collections_info:
                    continue

                collection = collections_info[collection_key]
                problems = collection.get('problems', {})

                # Get available block keys for this collection (not yet selected)
                available_block_keys = []
                for problem_usage_key in problems.keys():
                    if problem_usage_key in usage_key_to_block_key:
                        block_key = usage_key_to_block_key[problem_usage_key]
                        if problem_usage_key not in used_problems:
                            available_block_keys.append((block_key, problem_usage_key))

                # If count is -1, select all available problems
                if count == -1:
                    num_to_select = len(available_block_keys)
                else:
                    num_to_select = min(count, len(available_block_keys))

                # Randomly select from available problems
                if num_to_select > 0:
                    selected_items = rand.sample(available_block_keys, num_to_select)
                    for block_key, usage_key in selected_items:
                        new_selected_keys.add(block_key)
                        used_problems.add(usage_key)

            # Determine what changed
            added_block_keys = new_selected_keys - selected_keys
            overlimit_block_keys = selected_keys - new_selected_keys
            selected_keys = new_selected_keys

            return {
                'selected': sorted(selected_keys),
                'invalid': sorted(invalid_block_keys),
                'overlimit': sorted(overlimit_block_keys),
                'added': sorted(added_block_keys),
            }
        else:
            # Old logic.
            return super().make_selection(selected, children, max_count)

    def selected_children(self):
        """
        Return a list of block_ids indicating which children have been selected to display to the current user.

        This method extends the parent implementation to support collection-based selection
        when max_count_per_collection and collections_info are configured.

        This reads and updates the "selected" field, which has user_state scope.

        Note: the return value (self.selected) contains block_ids. To get
        actual BlockUsageLocators, it is necessary to use self.children,
        because the block_ids alone do not specify the block type.
        """
        max_count = self.max_count
        if max_count < 0:
            max_count = len(self.children)

        # Init of new logic for selecting childrens by collection.
        max_count_per_collection = None
        if self.max_count_per_collection:
            if self.validate_max_count_per_collection(self.max_count_per_collection):
                max_count_per_collection = self.max_count_per_collection
            else:
                logger.error("Invalid max_count_per_collection configuration; ignoring it.")

        block_keys = self.make_selection(
            self.selected,
            self.children,
            max_count,
            max_count_per_collection,
            self.collections_info
        )
        # End of new logic.

        self.publish_selected_children_events(
            block_keys,
            self.format_block_keys_for_analytics,
            self._publish_event,
        )

        if any(block_keys[changed] for changed in ('invalid', 'overlimit', 'added')):
            # Save our selections to the user state, to ensure consistency:
            selected = block_keys['selected']
            self.selected = selected  # pylint: disable=attribute-defined-outside-init

        return self.selected

    def validate_max_count_per_collection(self, max_count_per_collection):
        """
        Validate max_count_per_collection field.

        Ensures all values are integers >= -1 and the keys are part of the collections_info.
        """
        collections = self.collections_info.keys()
        for key, value in max_count_per_collection.items():
            try:
                value = int(value)
            except (ValueError, TypeError):
                return False
            if value < -1 or key not in collections:
                return False
        return True
    
    @XBlock.json_handler
    def update_max_count_per_collection(self, data, _):
        """
        Update the max_count_per_collection setting from Studio.
        """
        if not isinstance(data, dict):
            return {"status": "error", "message": "Invalid data format"}

        if not self.validate_max_count_per_collection(data):
          return {"status": "error", "message": "Invalid configuration"}
        
        # Persist configuration (Scope.settings)
        self.max_count_per_collection = data

        modulestore = get_modulestore()
        modulestore.update_item(self, self.runtime.user_id)
        
        return {"status": "ok"}

