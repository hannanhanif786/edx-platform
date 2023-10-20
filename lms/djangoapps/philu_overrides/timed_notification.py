from django.urls import reverse
from django.conf import settings
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xmodule.modulestore.django import modulestore



def get_course_first_chapter_link(course, request=None):
    """
    Helper function to get first chapter link in course enrollment email
    """
    from lms.djangoapps.philu_overrides.views.views import get_course_related_keys
    from lms.djangoapps.courseware.views.views import get_last_accessed_courseware
    from lms.djangoapps.courseware.courses import get_course_by_id
    from lms.djangoapps.courseware.access import has_access


    if not request:

        course_desc = get_course_by_id(course.id)
        first_chapter_url = ''
        first_section = ''
        if course_desc.get_children():
            first_chapter_url = course_desc.get_children()[0].scope_ids.usage_id.block_id
            if course_desc.get_children()[0].get_children():
                first_section = course_desc.get_children()[0].get_children()[0].scope_ids.usage_id.block_id

        course_target = reverse(
            'courseware_section',
            args=[course.id.to_deprecated_string(),
                  first_chapter_url,
                  first_section]
        )

        base_url = settings.LMS_ROOT_URL
        return base_url + course_target
    else:
        course_key = SlashSeparatedCourseKey.from_deprecated_string(
            course.id.to_deprecated_string())
        with modulestore().bulk_operations(course_key):
            if has_access(request.user, 'load', course):
                access_link = get_last_accessed_courseware(
                    get_course_by_id(course_key, 0),
                    request,
                    request.user
                )

                first_chapter_url, first_section = get_course_related_keys(
                    request, get_course_by_id(course_key, 0))
                first_target = reverse('courseware_section', args=[
                    course.id.to_deprecated_string(),
                    first_chapter_url,
                    first_section
                ])

                course_target = access_link if access_link is not None else first_target
            else:
                course_target = '/courses/' + course.id.to_deprecated_string()
        return course_target