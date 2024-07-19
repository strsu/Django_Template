from config.celery import app

from django.conf import settings
from django.utils import timezone

from api.common import cache

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import requests
import re
import os


def download_image(url, image_name, folder_name, headers={}):

    root = os.path.join(f"{settings.MEDIA_ROOT}", "aragon")
    folder_name = re.sub(r'[\\/:"*?<>|]', "", folder_name)
    folder_path = os.path.join(root, folder_name)

    os.makedirs(folder_path, exist_ok=True)

    image_name = re.sub(r'[\\/:"*?<>|]', "", image_name)

    try:
        # URL에 요청 보내기
        response = requests.get(url, headers=headers)
        # 응답 코드가 200(성공)인 경우에만 처리
        if response.status_code == 200:
            # 바이너리 파일로 쓰기
            with open(os.path.join(folder_path, image_name), "wb") as file:
                file.write(response.content)
        else:
            print(f"이미지 다운로드 실패, 상태 코드: {response.status_code}")
    except Exception as e:
        print(f"이미지 다운로드 중 오류 발생: {e}")


def get_cookies():

    # return [
    #     {
    #         "name": "PHPSESSID",
    #         "value": "d0bede8572d87658d1289588b15029eb",
    #         "domain": "aragonk.com",
    #         "path": "/",
    #         "expires": -1,
    #         "httpOnly": False,
    #         "secure": False,
    #         "sameSite": "None",
    #     }
    # ]

    cookies = cache.getKey("aragon")

    if cookies:
        return cookies

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()

        page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "Referer": "https://gall.dcinside.com/",
            }
        )

        page.goto("https://aragonk.com/xe/login")
        page.wait_for_load_state()  # the promise resolves after "load" event.

        page.locator('//*[@id="fo_login_widget"]/div/div/input[1]').fill("naeun")
        page.locator('//*[@id="fo_login_widget"]/div/div/input[2]').fill("lovral^^")
        page.locator(".swbuttonLogin").click()

        cookies = page.context.cookies()
        browser.close()

    cache.setKey("aragon", cookies, 60 * 60 * 6)

    return cookies


@app.task
def get_urls():

    meta = {}

    cookies = get_cookies()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Origin": "https://aragonk.com",
    }

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        page.set_extra_http_headers(headers)
        page.context.add_cookies(cookies)

        for _page in range(1, 2):

            root_url = f"https://aragonk.com/xe/?mid=o4&page={_page}"

            page.goto(root_url)
            page.wait_for_load_state()  # the promise resolves after "load" event.

            html = page.content()

            soup = BeautifulSoup(html, "lxml")

            li_list = soup.find("ul", "boardList").find_all("li")

            for li in li_list:
                thumb = li.find("div", "thumb")
                if thumb is None:
                    continue

                url = thumb.find("a").attrs.get("href")
                title = li.find("div", "title").find("a").attrs.get("title")

                sub_lis = li.find("ul", "meta").find_all("li")

                author = None
                date = None
                reading = None
                recommend = None
                for sl in sub_lis:
                    if "author" in sl.attrs.get("class"):
                        author = sl.text
                    elif "date" in sl.attrs.get("class"):
                        date = sl.text
                    elif "reading" in sl.attrs.get("class"):
                        reading = re.sub(r"[^0-9]", "", sl.text)
                    elif "recommend" in sl.attrs.get("class"):
                        recommend = re.sub(r"[^0-9]", "", sl.text)

                meta[url] = {
                    "title": title,
                    "author": author,
                    "date": date,
                    "reading": reading,
                    "recommend": recommend,
                }

                print(
                    f"{title}, 작성자: {author}, 날짜: {date}, 조회수: {reading}, 추천: {recommend}"
                )

                page.goto(url)
                page.wait_for_load_state()  # the promise resolves after "load" event.

                content_html = page.content()
                content_soup = BeautifulSoup(content_html, "lxml")

                imgs = content_soup.find("div", "view_content").find_all("img")

                for img in imgs:
                    img_name = img.attrs.get("title").replace(":", "").replace(" ", "_")
                    img_src = img.attrs.get("src")

                    download_image(img_src, img_name, author, headers)

        browser.close()
