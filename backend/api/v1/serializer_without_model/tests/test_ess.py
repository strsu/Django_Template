from django.test import TestCase
from rest_framework.test import APIClient

from api.v1.user.models import User

# python3 manage_local.py test api/v1/serializer_without_model/tests


class EssSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="admin", email="admin", password="admin"
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.admin)
        self.url = "/api/v1/serializerWithoutModel/ess/"
        self.url2 = "http://localhost/api/v1/serializerWithoutModel/ess/"
        self.headers = {"Content-Type": "application/json"}

    def test_valid_data(self):
        data = [
            {
                "ess_cap": 31.2,
                "ess_soc_l_lim": 0.02,
                "ess_soc_h_lim": 0.1,
                "pcs_cap": 12.12,
                "pcs_h_lim": 0.29,
                "ch_start": 3,
                "ch_end": 4,
                "dch_start": 1,
                "dch_end": 4,
                "ess_mfr": "sdf",
                "pcs_mfr": "sdf",
                "out_ctrl_feat": "afds",
                "ch_min_capacity": 2,
                "ch_max_capacity": 3,
                "dch_min_capacity": 2,
                "dch_max_capacity": 3,
            }
        ]
        # format=json을 안 하면 str로 넘어가서 dict로 인식을 못 한다.
        response = self.client.post(
            self.url, headers=self.headers, data=data, format="json"
        )

        self.assertEqual(response.status_code, 200)
