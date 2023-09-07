"""Models for the util app. """

import json

import gzip
import logging
from io import BytesIO

from config_models.models import ConfigurationModel
from django.db import models
from django.utils.text import compress_string
from opaque_keys.edx.django.models import CreatorMixin

from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class RateLimitConfiguration(ConfigurationModel):
    """
    Configuration flag to enable/disable rate limiting.

    Applies to Django Rest Framework views.

    This is useful for disabling rate limiting for performance tests.
    When enabled, it will disable rate limiting on any view decorated
    with the `can_disable_rate_limit` class decorator.

    .. no_pii:
    """
    class Meta(ConfigurationModel.Meta):
        app_label = "util"


def decompress_string(value):
    """
    Helper function to reverse CompressedTextField.get_prep_value.
    """

    try:
        val = value.encode('utf').decode('base64')
        zbuf = BytesIO(val)
        zfile = gzip.GzipFile(fileobj=zbuf)
        ret = zfile.read()
        zfile.close()
    except Exception as e:  # lint-amnesty, pylint: disable=broad-except
        logger.error('String decompression failed. There may be corrupted data in the database: %s', e)
        ret = value
    return ret


class CompressedTextField(CreatorMixin, models.TextField):
    """
    TextField that transparently compresses data when saving to the database, and decompresses the data
    when retrieving it from the database.
    """

    def get_prep_value(self, value):
        """
        Compress the text data.
        """
        if value is not None:
            if isinstance(value, str):
                value = value.encode('utf8')
            value = compress_string(value)
            value = value.encode('base64').decode('utf8')
        return value

    def to_python(self, value):
        """
        Decompresses the value from the database.
        """
        if isinstance(value, str):
            value = decompress_string(value)

        return value

"""
All models for custom settings
"""

class CustomSettingsManager(models.Manager):
    """
    Course Custom Settings Manager
    """
    def is_mini_lesson(self, course_key):
        """
        This method checks course with course_key if it is mini lesson or not

        Args:
            course_key (CourseKey, str): Course key
        Returns:
            bool: True if course is mini lesson else False
        """
        if isinstance(course_key, (str, unicode)):
            course_key = CourseKey.from_string(course_key)
        return self.get_queryset().filter(id=course_key, is_mini_lesson=True).exists()


class CustomSettings(models.Model):
    """
    Extra Custom Settings for each course
    """
    id = CourseKeyField(max_length=255, db_index=True, primary_key=True)
    is_featured = models.BooleanField(default=False)
    show_grades = models.BooleanField(default=True)
    enable_enrollment_email = models.BooleanField(default=True)
    auto_enroll = models.BooleanField(default=False)
    tags = models.CharField(max_length=255, null=True, blank=True)
    course_short_id = models.IntegerField(null=False, unique=True)
    seo_tags = models.TextField(null=True, blank=True)
    course_open_date = models.DateTimeField(null=True)
    is_mini_lesson = models.BooleanField(default=False)

    objects = CustomSettingsManager()

    # class Meta:
        # app_label = 'custom_settings'

    def __unicode__(self):
        return '{} | {}'.format(self.id, self.is_featured)

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        # This means that the model isn't saved to the database yet
        if self._state.adding and not self.course_short_id:
            # Get the maximum course_short_id value from the database
            last_id = CustomSettings.objects.all().aggregate(largest=models.Max('course_short_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                course_short_id = last_id + 1
                self.course_short_id = course_short_id

            else:
                self.course_short_id = 100

        super(CustomSettings, self).save(*args, **kwargs)

    def get_course_meta_tags(self):
        """
        Extract and get course meta tags from seo_tags, if seo_tags is empty return empty course meta tags

        Returns:
            dict: Course meta tags
        """
        title, description, keywords, robots, utm_params = "", "", "", "", {}
        if self.seo_tags:
            _json_tags = json.loads(self.seo_tags)
            title = _json_tags.get("title", title)
            description = _json_tags.get("description", description)
            keywords = _json_tags.get("keywords", keywords)
            robots = _json_tags.get("robots", robots)
            utm_params = {key: _json_tags[key] for key in _json_tags.keys() if 'utm_' in key}

        return {
            "title": title,
            "description": description,
            "keywords": keywords,
            "robots": robots,
            "utm_params": utm_params
        }
