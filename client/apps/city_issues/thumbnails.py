"""
This module create thumbnails
"""
import os.path
from PIL import Image, ImageOps
import StringIO

from django.conf import settings


def create_thumbnail(issue_file, title, url):
    head, tail = os.path.split(url)
    filename = "thumb-{}".format(tail)

    box = (240, 190)
    image = Image.open(issue_file)
    image = ImageOps.fit(image, box, Image.ANTIALIAS)
    image.save(os.path.join(settings.MEDIA_ROOT, 'uploads', title, filename), format=image.format)
