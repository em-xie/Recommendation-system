import requests
from api.config import config


def get_anime(user_id):
    params = {}
    if user_id is not None:
        params['user_id'] = user_id
        # print(params)
        # print(config['recall_endpoint'] + '/recall')
    res = requests.get(config['rank_endpoint'] + '/rank', params=params)
    res.raise_for_status()
    return res.json()


def get_similar_anime(anime_id):
    params = {}

    params['anime_id'] = anime_id
        # print(params)
        # print(config['recall_endpoint'] + '/recall')
    res = requests.get(config['recall_endpoint'] + '/sim', params=params)
    res.raise_for_status()
    return res.json()