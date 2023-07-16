import os

from api.v1.rating.tasks import transcoding_task


def mkdir(path):
    os.makedirs(path, exist_ok=True)


async def save_bytes(raw, flag, path, filename=""):
    mkdir(path)
    if flag == 2:
        # 파일 전송 중
        file = open(os.path.join(path, filename), "ab")
        file.write(raw)
        file.close()
    elif flag == 1:
        # 파일 전송 시작
        file = open(os.path.join(path, filename), "wb")
        file.close()
    elif flag == 0:
        # 파일 전송 종료
        transcoding_task.delay(filename)
    return filename
