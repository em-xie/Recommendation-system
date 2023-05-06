from recall.context import Context
from typing import List
import recall.strategy as strategy
import concurrent.futures

strategies: List[strategy.RecallStrategy] = [
    # strategy.SimpleRecallStrategy(),
    strategy.MostRatedStrategy(),
    strategy.HighRatedStrategy()
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
    stra = strategy.SimilarAnimeStrategy()
    return stra.recall(context,n)
