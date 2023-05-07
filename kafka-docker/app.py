from flask import Flask, request
from datetime import datetime
from kafka import KafkaProducer
from json import dumps

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

@app.route("/clicks", methods=['POST'])
def post_clicks():
    # data: { user_id, anime_id }
    data = request.json
    data['happened_at'] = int(datetime.timestamp(datetime.now()))
    print(data)

    producer.send('clicks', value=data)

    return 'ok'

@app.route("/views", methods=['POST'])
def post_views():
    # data: { user_id, anime_id }
    data = request.json
    data['happened_at'] = int(datetime.timestamp(datetime.now()))
    print(data)

    producer.send('views', value=data)

    return 'ok'
