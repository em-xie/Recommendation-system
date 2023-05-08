from typing import Tuple
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col, collect_list, udf
import numpy as np
from recall.config import config
from pyspark.ml.feature import Word2Vec


def train_item2vec(anime_seq: DataFrame, rating_df: DataFrame) -> Tuple[DataFrame, DataFrame]:
    model_config = config['item2vec']
    # spark训练 维度 反复训练几次 窗口大小
    word2vec = Word2Vec(vectorSize=model_config['vector_size'], maxIter=model_config['max_iter']
                        , windowSize=model_config['windowSize'])
    word2vec.setInputCol('anime_ids')
    word2vec.setOutputCol('anime_ids_vec')
    model = word2vec.fit(anime_seq)
    item_emb_df = model.getVectors()
    # embedding
    item_vec = model.getVectors().collect()
    item_emb = {}
    # 转成字典
    for item in item_vec:
        item_emb[item.word] = item.vector.toArray()

    # 传回
    @udf(returnType='array<float>')
    def build_user_emb(anime_seq):
        # id映射 anime_seq中的id到anime_embs
        anime_embs = [item_emb[aid] if aid in item_emb else [] for aid in anime_seq]
        # 求均值 过滤
        anime_embs = list(filter(lambda l: len(l) > 0, anime_embs))
        ret = np.mean(anime_embs, axis=0).tolist()

        return ret

    user_emb_df = rating_df \
        .where('rating > 7') \
        .groupBy('user_id') \
        .agg(
        collect_list(col('anime_id').cast('string')).alias('anime_ids')
    ) \
        .withColumn('user_emb', build_user_emb(col('anime_ids')))

    return (
        item_emb_df,
        user_emb_df
    )
