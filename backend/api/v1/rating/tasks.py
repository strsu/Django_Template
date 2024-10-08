from celery import shared_task

from api.v1.rating.models import Movie
from api.v1.chat.service.socket_manager import SocketManager

from django.conf import settings

import os
import datetime
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

"""
    코드가 변경되면 celery worker도 재시작 해줘야 된다.
"""

MEDIA_ROOT = settings.MEDIA_ROOT


def monitor(ffmpeg, duration, time_, time_left, process):
    """
    This function allows you to handle the transcoding process according to your needs.

    Examples:
        1. Logging or printing ffmpeg log
        logging.info(ffmpeg) or print(ffmpeg)

        2. Handling Process object based on specific events
        if "something happened":
            process.terminate()

        3. Sending email notifications about completion time
            if time_left > 3600 and not already_send:
            # Send email if process takes more than an hour
                ready_time = time_left + time.time()
                Email.send(
                    email='someone@somedomain.com',
                    subject='Your video will be ready by %s' % datetime.timedelta(seconds=ready_time),
                    message='Your video takes more than %s hour(s) ...' % round(time_left / 3600)
                )
               already_send = True

        4. Creating a progress bar or displaying other parameters to users
            Socket.broadcast(
                address=127.0.0.1
                port=5050
                data={
                    percentage = per,
                    time_left = datetime.timedelta(seconds=int(time_left))
                }
            )

    :param ffmpeg: ffmpeg command line
    :param duration: video duration
    :param time_: current time of transcoded video
    :param time_left: seconds left to finish transcoding
    :param process: subprocess object
    """
    per = round(time_ / duration * 100)
    # print(
    #     "\rTranscoding...(%s%%) %s left [%s%s]"
    #     % (
    #         per,
    #         datetime.timedelta(seconds=int(time_left)),
    #         "#" * per,
    #         "-" * (100 - per),
    #     )
    # )

    SocketManager.info(
        {"percentage": per, "left_time": datetime.timedelta(seconds=int(time_left))}
    )


@shared_task
def transcoding_task(filename):
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
    dash.output(os.path.join(save_path, "dash.mpd"), monitor=monitor)

    movie = Movie.actives.create(title=filename)

    return None
