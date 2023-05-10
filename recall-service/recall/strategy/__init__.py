from recall.strategy.recall_strategy import RecallStrategy
from recall.strategy.simple_strategy import SimilarAnimeStrategy
from recall.strategy.similar_anime_strategy import SimpleRecallStrategy
from recall.strategy.most_rated_strategy import MostRatedStrategy
from recall.strategy.high_rated_strategy import HighRatedStrategy
from recall.strategy.user_embedding_strategy import UserEmbeddingStrategy
from recall.strategy.recent_click_strategy import RecentClickStrategy
__all__ = {
    RecallStrategy,
    SimilarAnimeStrategy,
    SimpleRecallStrategy,
    MostRatedStrategy,
    HighRatedStrategy,
    UserEmbeddingStrategy,
    RecentClickStrategy

}