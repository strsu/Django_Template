from datetime import datetime, timedelta
import time
import pytz

import os

import base64
import string
import random


from django.conf import settings

MEDIA_ROOT = settings.MEDIA_ROOT


def generate_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def mkdir(path):
    os.makedirs(path, exist_ok=True)


def read_base64(filename):
    path = os.path.join(MEDIA_ROOT, f"board")

    with open(os.path.join(path, filename), "r") as img:
        # 가끔 bytes로 변환되는 것을 방지하기 위해 ascii로 디코딩을 해주는 게 좋은 것 같다.
        base64_string = img.read()  # base64.b64encode(img.read())  # .decode("ascii")

    return base64_string


def save_base64(base64_string, filename):
    path = os.path.join(MEDIA_ROOT, f"board")

    # decoded_data = base64.b64decode(base64_string)
    img_file = open(os.path.join(path, filename), "w")
    img_file.write(base64_string)
    img_file.close()


def unixtime_to_kst(unixtime):
    return datetime.fromtimestamp(unixtime, pytz.timezone("Asia/Seoul"))  # KST로 변환


def kst_to_unixtime(kst_time_str):
    # KST 시간 문자열을 datetime 객체로 변환
    kst = pytz.timezone("Asia/Seoul")
    kst_time = datetime.strptime(kst_time_str, "%Y-%m-%dT%H:%M:%S")  # KST 시간 형식
    kst_time = kst.localize(kst_time)  # KST 시간대 지정

    # UTC로 변환 후 Unix 타임스탬프로 변환
    utc_time = kst_time.astimezone(pytz.utc)
    unix_time = int(utc_time.timestamp() * 1000)  # 밀리초 단위로 변환
    return unix_time


def now_unixtime():
    # 현재 Unix 타임스탬프 (초 단위)
    current_unix_time = time.time()

    # Unix 타임스탬프를 UTC에서 KST로 변환
    utc_time = datetime.fromtimestamp(current_unix_time, pytz.utc)  # UTC 시간
    kst_time = utc_time.astimezone(pytz.timezone("Asia/Seoul"))  # KST로 변환

    # KST 시간을 다시 Unix 타임스탬프 (밀리초 단위)로 변환
    unix_time_in_kst = int(kst_time.timestamp() * 1000)  # 밀리초 단위로 변환

    return unix_time_in_kst
