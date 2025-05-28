from typing import Dict, Type

from .algorithm_handler import AlgorithmHandler
from .centrality_algorithm_handlers import PageRankHandler, ArticleRankHandler, \
    DegreeCentralityHandler, ArticulationPointsHandler, BetweennessCentralityHandler, BridgesHandler, CELFHandler, \
    ClosenessCentralityHandler, EigenvectorCentralityHandler, HarmonicCentralityHandler, HITSHandler
from .path_algorithm_handlers import DijkstraShortestPathHandler


class AlgorithmRegistry:
    _handlers: Dict[str, Type[AlgorithmHandler]] = {
        # Centrality algorithms
        "article_rank": ArticleRankHandler,
        "articulation_points": ArticulationPointsHandler,
        "betweenness_centrality": BetweennessCentralityHandler,
        "bridges": BridgesHandler,
        "CELF": CELFHandler,
        "closeness_centrality": ClosenessCentralityHandler,
        "degree_centrality": DegreeCentralityHandler,
        "eigenvector_centrality": EigenvectorCentralityHandler,
        "pagerank": PageRankHandler,
        "harmonic_centrality": HarmonicCentralityHandler,
        "HITS": HITSHandler,
        # Path algorithms
        "find_shortest_path": DijkstraShortestPathHandler,
    }

    @classmethod
    def get_handler(cls, name: str, db_url: str, username: str, password: str) -> AlgorithmHandler:
        handler_class = cls._handlers.get(name)
        if handler_class is None:
            raise ValueError(f"Unknown tool: {name}.")
        return handler_class(db_url, username, password)