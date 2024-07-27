import os
import time
import base64

from django.conf import settings

STATIC_ROOT = settings.STATIC_ROOT


def mkdir(path):
    os.makedirs(path, exist_ok=True)


def image_to_base64(user_id, filename, is_thumbnail=False):
    path = os.path.join(STATIC_ROOT, f"img/{user_id}")
    if is_thumbnail:
        path = os.path.join(STATIC_ROOT, f"thumbnail/{user_id}")

    with open(os.path.join(path, filename), "rb") as img:
        # 가끔 bytes로 변환되는 것을 방지하기 위해 ascii로 디코딩을 해주는 게 좋은 것 같다.
        base64_string = base64.b64encode(img.read()).decode("ascii")

    return base64_string


def save_base64(base64_string, room):
    path = os.path.join(STATIC_ROOT, f"chat/img/{room}")
    mkdir(path)
    # 데이터 부분 분리
    # base64_string = "data:image/jpeg;base64,/9j/4AAQSkZJRg
    ext, img_data = base64_string.split(",")
    ext = ext.split("/")[1][:-7]
    filename = f"{room}_{str(time.time())}.{ext}"
    # decode base64 string data
    decoded_data = base64.b64decode((img_data))
    # write the decoded data back to original format in  file
    img_file = open(os.path.join(path, filename), "wb")
    img_file.write(decoded_data)
    img_file.close()


async def save_bytes(raw, room, flag, user_token, filename=""):
    path = os.path.join(STATIC_ROOT, f"chat/img/{room}")
    mkdir(path)
    print(f"path: {path}")
    if flag == 2:
        # 파일 전송 중
        img_file = open(os.path.join(path, user_token), "ab")
        img_file.write(raw)
        img_file.close()
    elif flag == 1:
        # 파일 전송 시작
        img_file = open(os.path.join(path, user_token), "wb")
        img_file.close()
    elif flag == 0:
        # 파일 전송 종료
        filename = f"{room}_{str(time.time())}_{filename}"
        os.rename(os.path.join(path, user_token), os.path.join(path, filename))
    return filename
