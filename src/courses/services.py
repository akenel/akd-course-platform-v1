from django.db.models import Q
from .models import Course, Lesson, PublishStatus

# Service functions for Course and Lesson models

# Get all published courses
def get_publish_courses():
    """
    Retrieve all courses with a published status.
    """
    return Course.objects.filter(status=PublishStatus.PUBLISHED)

# Get course details by course_id
def get_course_detail(course_id=None):
    """
    Retrieve the details of a specific course by its public ID.
    
    Args:
        course_id (str): The public ID of the course.
    
    Returns:
        Course: The course object if found, otherwise None.
    """
    if course_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.get(
            status=PublishStatus.PUBLISHED,
            public_id=course_id
        )
    except Course.DoesNotExist:
        pass
    return obj

# Get lessons for a specific course
def get_course_lessons(course_obj=None):
    """
    Retrieve all lessons for a specific course that are either published or coming soon.
    
    Args:
        course_obj (Course): The course object.
    
    Returns:
        QuerySet: A queryset of lessons.
    """
    lessons = Lesson.objects.none()
    if not isinstance(course_obj, Course):
        return lessons # Return empty lessons if course_obj is not a Course instance
    lessons = course_obj.lesson_set.filter(
        course__status=PublishStatus.PUBLISHED,
        status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON]
    )
    return lessons

# Get lesson details by course_id and lesson_id
def get_lesson_detail(course_id=None, lesson_id=None):
    """
    Retrieve the details of a specific lesson by its public ID and the course's public ID.
    
    Args:
        course_id (str): The public ID of the course.
        lesson_id (str): The public ID of the lesson.
    
    Returns:
        Lesson: The lesson object if found, otherwise None.
    """
    if lesson_id is None and course_id is None:
        return None
    obj = None
    try:
        obj = Lesson.objects.get(
            course__public_id=course_id,
            course__status=PublishStatus.PUBLISHED,
            status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],
            public_id=lesson_id
        )
    except Lesson.DoesNotExist as e:
        print("lesson detail", e)
        pass
    return obj
