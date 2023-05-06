from flask import Flask,jsonify,request
from rank.service import rank_service
from rank.context import Context

# __name__ = 'rank-service'
# app = Flask(__name__)

app = Flask('rank-service')

@app.route("/rank")
def get_anime():
    user_id = request.args.get('user_id',type=int)
    print(f'Calling user {user_id}...')
    context = Context(user_id)
    return jsonify(rank_service.anime_rank(context,20))


if __name__ == 'main':
    app.run(debug=True,host='127.0.0.1',port=5001)




