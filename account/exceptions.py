from rest_framework.exceptions import APIException
from rest_framework import status


class ProgrammingLanguageNotFound(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = "programming language not found"
    default_code = "programming language not found"
