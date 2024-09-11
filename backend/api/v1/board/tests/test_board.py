from django.test import TestCase


# Create your tests here.
class TestBoardApiView(TestCase):
    @classmethod
    def setUpTestData(cls): ...

    def test_게시판조회(self):
        print(globals()["getcontext"]())
