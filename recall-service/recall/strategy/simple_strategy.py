from recall.strategy.recall_strategy import RecallStrategy
import recall.dataset.anime as dataset
from recall.context import Context
from typing import List

(anime_df, _) = dataset.load_dataset()
sorted_df = anime_df.sort_index()


class SimilarAnimeStrategy(RecallStrategy):

    def name(self):
        return 'Simple Anime'

    def recall(self, context: Context, n=20) -> List[int]:
        # 返回和目标动漫id相近的结果
        anime_ioc = sorted_df.index.get_loc(context.anime_id)
        from_index = anime_ioc
        if from_index + n > len(sorted_df):
            from_index = len(sorted_df) - n

        return sorted_df.iloc[from_index: from_index + n].index.to_list()
