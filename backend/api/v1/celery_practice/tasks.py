from celery import shared_task

from django.conf import settings

import os

"""
    코드가 변경되면 celery worker도 재시작 해줘야 된다.
"""

STATIC_ROOT = settings.STATIC_ROOT
MEDIA_ROOT = settings.MEDIA_ROOT


@shared_task
def file_task(filename):
    f = open(os.path.join(STATIC_ROOT, f"{filename}.log"), "w", encoding="utf-8")
    f.write("test")
    f.close()

    return None
