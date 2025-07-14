import logging
from typing import Dict, Any

from graphdatascience import GraphDataScience

from .algorithm_handler import AlgorithmHandler
from .gds import projected_graph

logger = logging.getLogger("mcp_server_neo4j_gds")


class NodeSimilarityHandler(AlgorithmHandler):
    def node_similarity(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Node Similarity parameters: {kwargs}")
            node_similarity_result = gds.nodeSimilarity.stream(G, **kwargs)

        return node_similarity_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.node_similarity(
            self.db_url,
            self.username,
            self.password,
            similarityCutoff=arguments.get("similarityCutoff"),
            degreeCutoff=arguments.get("degreeCutoff"),
            upperDegreeCutoff=arguments.get("upperDegreeCutoff"),
            topK=arguments.get("topK"),
            bottomK=arguments.get("bottomK"),
            topN=arguments.get("topN"),
            bottomN=arguments.get("bottomN"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            similarityMetric=arguments.get("similarityMetric"),
            useComponents=arguments.get("useComponents"),
        )


class FilteredNodeSimilarityHandler(AlgorithmHandler):
    def filtered_node_similarity(
        self, db_url: str, username: str, password: str, **kwargs
    ):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Filtered Node Similarity parameters: {kwargs}")
            filtered_node_similarity_result = gds.nodeSimilarity.filtered.stream(
                G, **kwargs
            )

        return filtered_node_similarity_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.filtered_node_similarity(
            self.db_url,
            self.username,
            self.password,
            sourceNodeFilter=arguments.get("sourceNodeFilter"),
            targetNodeFilter=arguments.get("targetNodeFilter"),
            similarityCutoff=arguments.get("similarityCutoff"),
            degreeCutoff=arguments.get("degreeCutoff"),
            upperDegreeCutoff=arguments.get("upperDegreeCutoff"),
            topK=arguments.get("topK"),
            bottomK=arguments.get("bottomK"),
            topN=arguments.get("topN"),
            bottomN=arguments.get("bottomN"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            similarityMetric=arguments.get("similarityMetric"),
            useComponents=arguments.get("useComponents"),
        )


class KNearestNeighborsHandler(AlgorithmHandler):
    def k_nearest_neighbors(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"K-Nearest Neighbors parameters: {kwargs}")
            k_nearest_neighbors_result = gds.knn.stream(G, **kwargs)

        return k_nearest_neighbors_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_nearest_neighbors(
            self.db_url,
            self.username,
            self.password,
            nodeProperties=arguments.get("nodeProperties"),
            topK=arguments.get("topK"),
            sampleRate=arguments.get("sampleRate"),
            deltaThreshold=arguments.get("deltaThreshold"),
            maxIterations=arguments.get("maxIterations"),
            randomJoins=arguments.get("randomJoins"),
            initialSampler=arguments.get("initialSampler"),
            similarityCutoff=arguments.get("similarityCutoff"),
            perturbationRate=arguments.get("perturbationRate"),
        )


class FilteredKNearestNeighborsHandler(AlgorithmHandler):
    def filtered_k_nearest_neighbors(
        self, db_url: str, username: str, password: str, **kwargs
    ):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Filtered K-Nearest Neighbors parameters: {kwargs}")
            filtered_k_nearest_neighbors_result = gds.knn.filtered.stream(G, **kwargs)

        return filtered_k_nearest_neighbors_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.filtered_k_nearest_neighbors(
            self.db_url,
            self.username,
            self.password,
            sourceNodeFilter=arguments.get("sourceNodeFilter"),
            targetNodeFilter=arguments.get("targetNodeFilter"),
            nodeProperties=arguments.get("nodeProperties"),
            topK=arguments.get("topK"),
            sampleRate=arguments.get("sampleRate"),
            deltaThreshold=arguments.get("deltaThreshold"),
            maxIterations=arguments.get("maxIterations"),
            randomJoins=arguments.get("randomJoins"),
            initialSampler=arguments.get("initialSampler"),
            similarityCutoff=arguments.get("similarityCutoff"),
            perturbationRate=arguments.get("perturbationRate"),
            seedTargetNodes=arguments.get("seedTargetNodes"),
        )
