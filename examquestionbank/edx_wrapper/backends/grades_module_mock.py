"""Mock backend for grades for testing purposes."""


class MockCourseData:
    """Mock CourseData class for testing."""

    def __init__(self, user, course_key):
        """Initialize mock course data."""
        self.user = user
        self.course_key = course_key


class MockSubsectionGrade:
    """Mock SubsectionGrade class for testing."""

    def __init__(self):
        """Initialize mock subsection grade."""
        self.percent_graded = 0.75  # Mock 75% grade


class MockSubsectionGradeFactory:
    """Mock SubsectionGradeFactory class for testing."""

    def __init__(self, student, course_data=None):
        """Initialize mock grade factory."""
        self.student = student
        self.course_data = course_data

    def create(self, _subsection_block):
        """Create a mock subsection grade."""
        return MockSubsectionGrade()


def get_subsection_grade_factory():
    """Return mock SubsectionGradeFactory class."""
    return MockSubsectionGradeFactory


def get_course_data():
    """Return mock CourseData class."""
    return MockCourseData
