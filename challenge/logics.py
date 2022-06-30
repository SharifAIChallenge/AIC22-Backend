import requests

from django.conf import settings


def upload_code(file):
    """
    This function uploads a code file to infrastructure synchronously
    :param file: File field from TeamSubmission model
    :return: file token or raises error with error message
    """

    response = requests.post(
        settings.GATEWAY_HOST + "/upload/code",
        files={'file': file},
        headers={'Authorization': f'Token {settings.GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Upload Code ====")

    return response.json()['code_id']


def compile_submissions(submissions):
    # todo: complete this method
    pass
