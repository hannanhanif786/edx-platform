"""
Contain celery tasks
"""
from celery import shared_task
from django.contrib.auth import get_user_model
from opaque_keys.edx.locator import CourseKey
from lms.djangoapps.courseware.courses import get_course_with_access
from openedx.core.djangoapps.django_comment_common.comment_client.thread import Thread
from .utils import DiscussionNotificationSender


User = get_user_model()


@shared_task
def send_thread_created_notification(thread_id, course_key_str, user_id):
    """
    Send notification when a new thread is created
    """
    thread = Thread(id=thread_id).retrieve()
    user = User.objects.get(id=user_id)
    course_key = CourseKey.from_string(course_key_str)
    course = get_course_with_access(user, 'load', course_key, check_if_enrolled=True)
    notification_sender = DiscussionNotificationSender(thread, course, user)
    thread_type = thread.attributes['thread_type']
    notification_type = (
        "new_question_post"
        if thread_type == "question"
        else ("new_discussion_post" if thread_type == "discussion" else "")
    )
    notification_sender.send_new_thread_created_notification(notification_type)
