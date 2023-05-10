from recall.context import Context
from typing import List
import recall.strategy as strategy
import concurrent.futures
import time
from recall.model.lsh import get_item_lsh
from recall.dataset.embedding import get_one_item_embedding
from recall import util
strategies: List[strategy.RecallStrategy] = [
    # strategy.SimpleRecallStrategy(),
    strategy.MostRatedStrategy(),
    strategy.HighRatedStrategy(),
    strategy.UserEmbeddingStrategy(),
    strategy.RecentClickStrategy
]


def anime_recall(context: Context, n=20) -> List[int]:
    experiment_strategies = strategies[1:]
    bucket = util.bucketize()
    if bucket == 1:
        experiment_strategies = strategies
    print(f"user_id{context.user_id},recall exp bucket {bucket}")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        outputs = executor.map(lambda s: s.recall(context, n), experiment_strategies)
        # outputs: [[1,2,3],[3,4,5]]
        outputs = [aid for l in outputs for aid in l]
        # outputs:[1,2,3,3,4,5,]
        outputs = list(dict.fromkeys(outputs))
        return [{'anime_id':id,'ab:recall':bucket} for id in outputs]


def similar_animes(context: Context, n=20) -> List[int]:

    lsh = get_item_lsh()
    targer_item_emb = get_one_item_embedding(context.anime_id)
    return lsh.search(targer_item_emb,n=n)