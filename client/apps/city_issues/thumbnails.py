"""
This module create thumbnails
"""
import os.path

from django.conf import settings
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill


class Thumbnail(ImageSpec):
    """Class Thumbnail"""
    processors = [ResizeToFill(243, 150)]
    format = 'JPEG'
    options = {'quality': 60}


def create_thumbnail(issue_file, title, name):
    image_generator = Thumbnail(source=issue_file)
    result = image_generator.generate()
    filename = "-".join(["thumb", name])
    thumb_file = open(os.path.join(settings.MEDIA_ROOT, 'uploads', title, filename), 'w')
    thumb_file.write(result.read())
    thumb_file.close()
