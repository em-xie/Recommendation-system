from redis import Redis
import json

item_numeric_feature_prefix = 'rank:item:num'
user_numeric_feature_prefix = 'rank:user:num'
item_categorical_feature_prefix = 'rank:item:cat'
user_categorical_feature_prefix = 'rank:user:cat'

redis = Redis()

def __read_numeric_feartures(prefix,aid):
    key = f"{prefix}:{aid}"
    result = redis.hgetall(key)
    return {k.decode():float(v.decode()) for k,v in result.items()}

def get_item_numeric_features(item_id):
    return __read_numeric_feartures(item_numeric_feature_prefix,item_id)

def get_user_numeric_features(user_id):
    return __read_numeric_feartures(user_numeric_feature_prefix,user_id)

def __read_categorical_feature(prefix,aid):
    key = f"{prefix}:{aid}"
    result = redis.hgetall(key)
    return {k.decode():json.loads(v.decode()) for  k,v in result.items()}


def get_item_categorical_features(item_id):
    return __read_numeric_feartures(item_categorical_feature_prefix,item_id)

def get_user_categorical_features(user_id):
    return __read_numeric_feartures(user_categorical_feature_prefix,user_id)
