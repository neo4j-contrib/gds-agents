import logging
from typing import Dict, Any

from graphdatascience import GraphDataScience

from mcp_server.src.mcp_server_neo4j_gds.algorithm_handler import AlgorithmHandler
from mcp_server.src.mcp_server_neo4j_gds.gds import projected_graph

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_server_neo4j_gds.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('mcp_server_neo4j_gds')


class ConductanceHandler(AlgorithmHandler):
    def conductance(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Conductance parameters: {kwargs}")
            conductance = gds.conductance.stream(G, **kwargs)

        return conductance

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.article_rank(
            self.db_url,
            self.username,
            self.password,
            communityProperty=arguments.get("communityProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class HDBSCANHandler(AlgorithmHandler):
    def hdbscan(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"HDBSCAN parameters: {kwargs}")
            hdbscan_result = gds.hdbscan.stream(G, **kwargs)

        return hdbscan_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.hdbscan(
            self.db_url,
            self.username,
            self.password,
            nodeProperty=arguments.get("nodeProperty"),
            minClusterSize=arguments.get("minClusterSize"),
            samples=arguments.get("samples"),
            leafSize=arguments.get("leafSize"),
        )


class KCoreDecompositionHandler(AlgorithmHandler):
    def k_core_decomposition(self, db_url: str, username: str, password: str):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Running K-Core Decomposition")
            kcore_decomposition_result = gds.kcore_decomposition.stream(G)

        return kcore_decomposition_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_core_decomposition(
            self.db_url,
            self.username,
            self.password,
        )


class K1ColoringHandler(AlgorithmHandler):
    def k_1_coloring(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"K-1 Coloring parameters: {kwargs}")
            k1_coloring_result = gds.k1_coloring.stream(G, **kwargs)

        return k1_coloring_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_1_coloring(
            self.db_url,
            self.username,
            self.password,
            maxIterations=arguments.get("maxIterations"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )


class KMeansClusteringHandler(AlgorithmHandler):
    def k_means_clustering(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"K-Means Clustering parameters: {kwargs}")
            kmeans_clustering_result = gds.kmeans_clustering.stream(G, **kwargs)

        return kmeans_clustering_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_means_clustering(
            self.db_url,
            self.username,
            self.password,
            nodeProperty=arguments.get("nodeProperty"),
            k=arguments.get("k"),
            maxIterations=arguments.get("maxIterations"),
            deltaThreshold=arguments.get("deltaThreshold"),
            numberOfRestarts=arguments.get("numberOfRestarts"),
            initialSampler=arguments.get("initialSampler"),
            seedCentroids=arguments.get("seedCentroids"),
            computeSilhouette=arguments.get("computeSilhouette"),
        )
    

class LabelPropagationHandler(AlgorithmHandler):
    def label_propagation(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Label Propagation parameters: {kwargs}")
            label_propagation_result = gds.label_propagation.stream(G, **kwargs)

        return label_propagation_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.label_propagation(
            self.db_url,
            self.username,
            self.password,
            maxIterations=arguments.get("maxIterations"),
            nodeWeightProperty=arguments.get("nodeWeightProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            seedProperty=arguments.get("seedProperty"),
            consecutiveIds=arguments.get("consecutiveIds"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )
    

class LeidenHandler(AlgorithmHandler):
    def leiden(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Leiden parameters: {kwargs}")
            leiden_result = gds.leiden.stream(G, **kwargs)

        return leiden_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.leiden(
            self.db_url,
            self.username,
            self.password,
            maxLevels=arguments.get("maxLevels"),
            gamma=arguments.get("gamma"),
            theta=arguments.get("theta"),
            tolerance=arguments.get("tolerance"),
            includeIntermediateCommunities=arguments.get("includeIntermediateCommunities"),
            seedProperty=arguments.get("seedProperty"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )