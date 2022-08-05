import requests

from AIC22_Backend import settings
from challenge.models import Match


def upload_code(submission):
    """
    This function uploads a code file to infrastructure synchronously
    :param submission: Submission Model
    :return: file token or raises error with error message
    """
    print('----- trying to upload code to infra ---- ', submission.id, submission.language)
    response = requests.post(
        settings.INFRA_GATEWAY_HOST + "/upload/code",
        files={'file': submission.file},
        data={'language': submission.language},
        headers={'Authorization': f'{settings.INFRA_GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Upload Code ====")

    return response.json()['code_id']


def upload_map(file, config_file):
    print("ommad upload kone", file.size)
    response = requests.post(
        settings.INFRA_GATEWAY_HOST + "/upload/map",
        files={'file': file, 'json-file': config_file},
        headers={'Authorization': f'{settings.INFRA_GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Upload Map ====")

    return response.json()['map_id']


def run_match(match: Match, priority=0):
    response = requests.post(
        settings.INFRA_GATEWAY_HOST + "/game/register",
        data={
            'map_id': match.match_info.map.infra_token,
            'player_ids': [
                match.match_info.team1_code.infra_token,  # in game id: 0
                match.match_info.team2_code.infra_token  # in game id: 1
            ],
        },
        params={'priority': priority},
        headers={'Authorization': f'{settings.INFRA_GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Run Game ====")

    return response.json()['game_id']


def download_code(file_infra_token):
    response = requests.get(
        settings.INFRA_GATEWAY_HOST + "/download/code",
        params={
            'code_id': file_infra_token
        },
        headers={'Authorization': f'{settings.INFRA_GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Download File ====")

    return response.json()['code']


def download_log(match_infra_token, file_infra_token=None):
    params = {
        'game_id': match_infra_token
    }
    if file_infra_token:
        params['player_id'] = file_infra_token
    response = requests.get(
        settings.INFRA_GATEWAY_HOST + "/download/log",
        params=params,
        headers={'Authorization': f'{settings.INFRA_GATEWAY_AUTH_TOKEN}'}
    )
    print(response.status_code, response.json(), "==== Download File ====")

    return response.json()['log']
