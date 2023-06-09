from posixpath import join
from os.path import join
import pandas as pd
# from recall.config import config
from functools import lru_cache
import os
from pyspark.sql.session import SparkSession
from recall.config import config
from functools import lru_cache
@lru_cache()
def load_dataset():

    # anime_df = pd.read_csv(config['dataset_path'] + '/anime.csv',index_col='anime_id')
    # rating_df = pd.read_csv(config['dataset_path'] + '/rating.csv')
    anime_df = pd.read_csv('E://PyCode/Recommendation-system/dataset/anime.csv',index_col='anime_id')
    rating_df = pd.read_csv('E://PyCode/Recommendation-system/dataset/rating.csv')

    return (anime_df,rating_df)


def spark_load_ratings(spark: SparkSession):
    return spark.read.csv(join('E://PyCode/Recommendation-system/dataset/rating.csv','rating.csv'),header=True,inferSchema=True)