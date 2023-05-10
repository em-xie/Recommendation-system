import rank.util.recall_service_client as recall_client
from random import sample
import rank.dataset.feature as feature
import numpy as np
import rank.model.mlp as mlp

model = mlp.MLPModel()

def anime_rank(context, n):
    user_id = context.user_id
    recall_res = recall_client.get_recall(user_id)

    if user_id is None:
        return recall_res

    user_num_features = feature.get_user_numeric_features(user_id)
    user_cat_features = feature.get_user_categorical_features(user_id)

    item_num_feature_list = [feature.get_item_numeric_features(item_id) for item_id in recall_res]
    item_cat_feature_list = [feature.get_item_categorical_features(item_id) for item_id in recall_res]

    module_inputs = __build_features(
        item_cat_feature_list,
        user_cat_features,
        item_num_feature_list,
        user_num_features
    )
    scores =model.predict(module_inputs)
    scores = [s[0] for  s in scores]
    item_with_score = list(zip(recall_res,scores))
    item_with_score = sorted(item_with_score,key=lambda x:x[1],reverse=True)
    item_with_score = list(filter(lambda x:x[1] >= 0.5,item_with_score))
    return [x[0] for x in item_with_score]

def __build_features(item_cats, user_cats, item_nums, user_nums):
    # x1
    x1 = [np.array(item['genres_multihot']) for item in item_cats]

    x2 = [np.array(user_cats['user_liked_genres_multihot'] for _ in item_cats)]

    x3 = [__get_item_nums(item_nums) for item in item_nums]
    x4 = [__get_user_nums(user_nums) for _ in item_nums]
    return [np.array(x1), np.array(x2), np.array(x3), np.array(x4)]


def __get_item_nums(item_num):
    return np.array([
        item_num['all_rating_min_max'],
        item_num['members_min_max'],
        item_num['aired_from_min_max'],
        item_num['aired_to_min_max']

    ])


def __get_user_nums(user_num):
    return np.array([
        user_num['user_rating_ave_min_max'],
        user_num['user_rating_std_min_max'],
        user_num['user_aired_from_min_max'],
        user_num['user_aired_to_min_max']
    ])
