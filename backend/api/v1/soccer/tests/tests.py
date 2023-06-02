from django.test import Client, TestCase
import base64

from api.v1.user.models import User


class SoccerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def tearDown(self):
        pass

    def test_get_data(self):
        client = Client()

        result = {
            "id": 5,
            "where": {
                "name": "test1",
                "address": "address",
                "latitude": 37.13343,
                "longitude": 127.21134,
            },
            "when": "2023-04-12",
            "level": 1,
            "score": 4.0,
            "memo": "svsdv",
            "picture": [],
            "video": [],
            "tags": [],
            "created_at": "2023-04-09T10:12:14.700741",
            "modified_at": "2023-05-20T08:50:17.132467",
            "deleted_at": None,
        }

        business_list = ["admin:admin"]
        for idx, business in enumerate(business_list):
            credentials = base64.b64encode(bytes(business, "utf-8")).decode("ascii")
            client.defaults["HTTP_AUTHORIZATION"] = "Basic " + credentials

            response = client.get(
                "/api/v1/soccer/5/",
            )
            self.assertEqual(response.json(), result)
