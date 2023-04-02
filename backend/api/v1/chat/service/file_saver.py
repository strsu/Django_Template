import time
import base64


def save_image(base64_string, room):
    # 데이터 부분 분리
    # base64_string = "data:image/jpeg;base64,/9j/4AAQSkZJRg
    ext, img_data = base64_string.split(",")
    ext = ext.split("/")[1][:-7]
    # decode base64 string data
    decoded_data = base64.b64decode((img_data))
    # write the decoded data back to original format in  file
    img_file = open(f"/opt/{room}_{str(time.time())}.{ext}", "wb")
    img_file.write(decoded_data)
    img_file.close()
