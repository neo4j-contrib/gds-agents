from typing import Dict, Type

from .algorithm_handler import AlgorithmHandler
from .centrality_algorithm_handlers import PageRankHandler, ArticleRankHandler, \
    DegreeCentralityHandler
from .path_algorithm_handlers import DijkstraShortestPathHandler


class AlgorithmRegistry:
    _handlers: Dict[str, Type[AlgorithmHandler]] = {
        "pagerank": PageRankHandler,
        "article_rank": ArticleRankHandler,
        "degree_centrality": DegreeCentralityHandler,
        "find_shortest_path": DijkstraShortestPathHandler,
        # ... other algorithms
    }

    @classmethod
    def get_handler(cls, name: str, db_url: str, username: str, password: str) -> AlgorithmHandler:
        handler_class = cls._handlers.get(name)
        if handler_class is None:
            raise ValueError(f"Unknown tool: {name}.")
        return handler_class(db_url, username, password)