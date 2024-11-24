from rest_framework.exceptions import APIException


class CustomException(APIException):
    """
    CustomException(detail="에러메세지", code=400)
    """

    pass
