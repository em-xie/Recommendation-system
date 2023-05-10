from flask import Flask, jsonify, request
from api import rank_service_client
from api.anime import get_anime
# __name__ = 'rank-service'
# app = Flask(__name__)

app = Flask('api-service')


@app.route("/")
def get_recommends():
    user_id = request.args.get('user_id',type=int)
    # print(f'Calling user {user_id}...')
    # context = Context(user_id)
    rec_animes = rank_service_client.get_anime(user_id)
    for item in rec_animes:
        item['anime'] = get_anime(item['anime_id'])
    res = rec_animes
    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

@app.route("/sim")
def get_similar_animes():
    anime_id = request.args.get('anime_id',type=int)
    # print(f'Calling user {user_id}...')
    # context = Context(user_id)
    if anime_id is None:
        return 'bad anime id',400
    sim_anime = rank_service_client.get_similar_anime(anime_id)
    for item in sim_anime:
        item['anime'] = get_anime(item['anime_id'])
    res = sim_anime
    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response


if __name__ == 'main':
    app.run(debug=True, host='127.0.0.1', port=5002)
