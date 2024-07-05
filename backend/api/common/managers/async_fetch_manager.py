import aiohttp
import asyncio
import json


class AsyncFetchManager:
    """
    usage
        fm = FetchManager()
        asyncio.run(fm.fetch_data([]))
    """

    def __init__(self, headers, semaphore=5, timeout=30):
        self.headers = headers
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(
            semaphore
        )  # 최대 5개의 동시 요청을 허용하는 Semaphore 생성

    async def _get_(self, session, url, params={}):
        try:
            async with self.semaphore:  # Semaphore를 사용하여 동시 접근을 제어
                async with session.get(
                    url, params=params, headers=self.headers, timeout=self.timeout
                ) as response:
                    if response.status >= 400:
                        print(f"Fail to Fetch - {response.status}\n\t res: {res}")
                        res = await response.text()
                        return None
                    res = await response.json()
                    return res
        except Exception as e:
            print(f"Fail to Fetch - {e}\n\t url: {url}")
            return None

    async def _post_(self, session, url, data):
        try:
            async with self.semaphore:  # Semaphore를 사용하여 동시 접근을 제어
                async with session.post(
                    url,
                    data=json.dumps(data),
                    headers=self.headers,
                    timeout=self.timeout,
                ) as response:
                    if response.status >= 400:
                        return None
                    res = response.status
                    return res
        except Exception as e:
            print(f"Fail to POST - {e}\n\t url: {url}")
            return None

    async def get_data(self, url, params: list):
        """
        param = {'key1': 'value1', 'key2': 'value2'}
        """
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            tasks = [self._get_(session, url, param) for param in params]
            responses = await asyncio.gather(*tasks)

        return responses

    async def post_data(self, url, payloads: list):
        """
        datas = {
            url : payload,
        }
        """
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            tasks = [self._post_(session, url, payload) for payload in payloads]
            responses = await asyncio.gather(*tasks)

        return responses
