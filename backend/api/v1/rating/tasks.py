from celery import shared_task

from api.v1.rating.models import Movie

from django.conf import settings

import os
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

"""
    코드가 변경되면 celery worker도 재시작 해줘야 된다.
"""

STATIC_ROOT = settings.STATIC_ROOT
MEDIA_ROOT = settings.MEDIA_ROOT


@shared_task
def test_task(filename):
    title, ext = filename.split(".")
    file_path = os.path.join(MEDIA_ROOT, "media")
    save_path = os.path.join(MEDIA_ROOT, title)
    os.makedirs(save_path, exist_ok=True)

    video = ffmpeg_streaming.input(os.path.join(file_path, filename))

    _144p = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    _240p = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
    _2k = Representation(Size(2560, 1440), Bitrate(6144 * 1024, 320 * 1024))
    _4k = Representation(Size(3840, 2160), Bitrate(17408 * 1024, 320 * 1024))

    dash = video.dash(Formats.h264())
    # dash.auto_generate_representations()
    dash.representations(_360p, _720p)
    dash.output(os.path.join(save_path, "dash.mpd"))

    return None
