# import os
#
# config = {
#     'dataset_path': os.environ['DATASET_PATH']
# }
# def config():
#     return None

config = {
    'redis': {
        'host': 'http://127.0.0.1',
        'port': 6379,
        'db': 'anime',
        'pwd': 123456
    },
    'item2vec':{
        'vector_size': 2,
        'max_iter': 2,
        'windowSize': 1
    },
    'deepwalk''sample_count':{
        5
    },
    'deepwalk''sample_length':{
        5
    }
}