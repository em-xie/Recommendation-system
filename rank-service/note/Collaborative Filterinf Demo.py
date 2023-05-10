import pandas as pd
import numpy as np

rating_df = pd.read_csv('E://PyCode//Recommendation-system//dataset//rating.csv')
rating_df = rating_df[(rating_df['rating'] > 0) & (rating_df['user_id'] != 42653)]
# rating_df
anime_df = pd.read_csv('E://PyCode//Recommendation-system//dataset//anime.csv')
# cf
r_df = rating_df.reset_index().pivot(index='user_id', columns='anime_id', values='rating').fillna(0)
# print(r_df)
r = r_df.to_numpy()
# svd
from scipy.sparse.linalg import svds

rating_mean = np.mean(r, axis=1)
r_demeaned = r - rating_mean.reshape(-1, 1)
U, sigma, Vt = svds(r_demeaned, k=20)
# 对角阵
sigma = np.diag(sigma)
# 3个矩阵相乘
preds = np.dot(np.dot(U, sigma), Vt) + rating_mean.reshape(-1, 1)
pred_df = pd.DataFrame(preds, columns=r_df.columns)
# print(pred_df)


def recommend_movie(pred_df, user_id, movie_df, origin_rating_df, num=5):
    user_index = user_id - 1
    sorted_user_preds = pred_df.iloc[user_index].sort_values(ascending=False)
    existing_user_ratings = origin_rating_df[origin_rating_df['user_id'] == user_id]
    existing_ratings_df = existing_user_ratings.merge(movie_df, how='left', left_on='anime_id', right_on='anime_id'). \
        sort_values(['rating'], ascending=False)
    print(f'User {user_id} has already rated {existing_ratings_df.shape[0]} movies')

    recommends = (movie_df[~movie_df['anime_df'].isin(existing_user_ratings['anime_id'])]). \
                     merge(sorted_user_preds.reset_index(), how='left', left_on='anime_id', right_on='anime_id'). \
                     rename(colums={user_index: 'Predictions'}). \
                     sort_values('Predictions', ascending=False). \
                     iloc[:num]
    return existing_ratings_df, recommends

anime_df = anime_df.rename(columns={'rating':'old_rating'})
already_rated,user_preds = recommend_movie(pred_df,426,anime_df,rating_df,num = 10)
print(already_rated)
print(user_preds)