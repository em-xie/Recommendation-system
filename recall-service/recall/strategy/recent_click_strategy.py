from recall.strategy.recall_strategy import RecallStrategy
from redis import Redis
from recall.model.lsh import get_item_lsh
from recall.dataset.embedding import get_one_item_embedding

class RecentClickStrategy(RecallStrategy):
    def __init__(self)->None:
        super().__init__()
        self.redis = Redis
        self.lsh=get_item_lsh()

    def name(self):
        return 'RecentClick'

    def recall(self,context,n=20):
        if context.user_id is None:
            return[]

        user_id = context.user_id
        redis_key = f'recent_click:{user_id}'
        recent_clicks = self.redis.hgetall(redis_key)
        recent_clickd_animed_ids = [int(k.decode()) for k in recent_clicks.keys()]
        num = int(n/len(recent_clickd_animed_ids))
        similar_animes = [self.similar_animes_for(aid,num)for aid in recent_clickd_animed_ids]

        return [id for l in similar_animes for id in l]

    def similar_animes_for(self,anime_id,n):
        anime_emb = get_one_item_embedding(anime_id)
        if anime_emb is None:
            return []

        similar_res = [id for id in self.lsh.search(anime_emb,n=n+1) if id != anime_id]
