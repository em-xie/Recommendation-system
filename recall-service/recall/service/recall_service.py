from recall.context import Context
from typing import List
import recall.strategy as strategy
import concurrent.futures
import time
from recall.model.lsh import get_item_lsh
from recall.dataset.embedding import get_one_item_embedding
strategies: List[strategy.RecallStrategy] = [
    # strategy.SimpleRecallStrategy(),
    strategy.MostRatedStrategy(),
    strategy.HighRatedStrategy(),
    strategy.UserEmbeddingStrategy()
]


def anime_recall(context: Context, n=20) -> List[int]:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        outputs = executor.map(lambda s: s.recall(context, n), strategies)
        # outputs: [[1,2,3],[3,4,5]]
        outputs = [aid for l in outputs for aid in l]
        # outputs:[1,2,3,3,4,5,]
        outputs = list(dict.fromkeys(outputs))
        return outputs


def similar_animes(context: Context, n=20) -> List[int]:

    lsh = get_item_lsh()
    targer_item_emb = get_one_item_embedding(context.anime_id)
    return lsh.search(targer_item_emb,n=n)