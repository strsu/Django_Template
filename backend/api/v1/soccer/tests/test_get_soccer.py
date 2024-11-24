from rest_framework.test import APIClient
from django.test import Client, TestCase
import base64

from django.contrib.auth import get_user_model

# python manage.py test api/v1/soccer/tests
# python manage.py test api/v1/soccer/tests --settings='config.settings.test_real_db'


class SoccerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test = get_user_model().objects.create_user(username="test", email="test", password="test")

    def setUp(self):
        self.client = APIClient()
        self.headers = {"Content-Type": "application/json"}

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
            "updated_at": "2023-05-20T08:50:17.132467",
            "deleted_at": None,
        }

        business_list = ["test:test"]
        for idx, business in enumerate(business_list):
            credentials = base64.b64encode(bytes(business, "utf-8")).decode("ascii")
            client.defaults["HTTP_AUTHORIZATION"] = "Basic " + credentials

            response = client.get(
                "/api/v1/soccer/5/",
            )
            self.assertEqual(response.json(), result)

    def test_get_data_v2(self):

        data = {
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
        }

        # self.client.force_login(self.test)
        self.client.force_authenticate(user=self.test)
        url = "/api/v1/soccer/"
        response = self.client.post(url, headers=self.headers, data=data, format="json")

        print(response.json())

        self.assertEqual(response.status_code, 201)
