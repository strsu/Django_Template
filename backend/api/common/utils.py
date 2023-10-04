import os
import time
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
