import requests
from rank.config import config


def get_recall(user_id):
    params = {}
    if user_id is not None:
        params['user_id'] = user_id
        # print(params)
        print(config['recall_endpoint'] + '/recall')
    res = requests.get(config['recall_endpoint'] + '/recall', params=params)
    return res.json()
