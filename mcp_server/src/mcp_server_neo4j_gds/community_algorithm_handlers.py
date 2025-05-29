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


class LocalClusteringCoefficientHandler(AlgorithmHandler):
    def local_clustering_coefficient(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Local Clustering Coefficient parameters: {kwargs}")
            local_clustering_coefficient_result = gds.local_clustering_coefficient.stream(G, **kwargs)

        return local_clustering_coefficient_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.local_clustering_coefficient(
            self.db_url,
            self.username,
            self.password,
            triangleCountProperty=arguments.get("triangleCountProperty"),
        )


class LouvainHandler(AlgorithmHandler):
    def louvain(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Louvain parameters: {kwargs}")
            louvain_result = gds.louvain.stream(G, **kwargs)

        return louvain_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.louvain(
            self.db_url,
            self.username,
            self.password,
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            seedProperty=arguments.get("seedProperty"),
            maxLevels=arguments.get("maxLevels"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
            includeIntermediateCommunities=arguments.get("includeIntermediateCommunities"),
            consecutiveIds=arguments.get("consecutiveIds"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )


class ModularityMetricHandler(AlgorithmHandler):
    def modularity_metric(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Modularity Metric parameters: {kwargs}")
            modularity_metric_result = gds.modularity_metric.stream(G, **kwargs)

        return modularity_metric_result
    
    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.modularity_metric(
            self.db_url,
            self.username,
            self.password,
            communityProperty=arguments.get("communityProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )
    

class ModularityOptimizationHandler(AlgorithmHandler):
    def modularity_optimization(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Modularity Optimization parameters: {kwargs}")
            modularity_optimization_result = gds.modularity_optimization.stream(G, **kwargs)

        return modularity_optimization_result
    
    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.modularity_optimization(
            self.db_url,
            self.username,
            self.password,
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
            seedProperty=arguments.get("seedProperty"),
            consecutiveIds=arguments.get("consecutiveIds"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )
    

class StronglyConnectedComponentsHandler(AlgorithmHandler):
    def strongly_connected_components(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Strongly Connected Components parameters: {kwargs}")
            strongly_connected_components_result = gds.strongly_connected_components.stream(G, **kwargs)

        return strongly_connected_components_result
    
    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.strongly_connected_components(
            self.db_url,
            self.username,
            self.password,
            consecutiveIds=arguments.get("consecutiveIds"),
        )


class TriangleCountHandler(AlgorithmHandler):
    def triangle_count(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Triangle Count parameters: {kwargs}")
            triangle_count_result = gds.triangle_count.stream(G, **kwargs)

        return triangle_count_result
    
    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.triangle_count(
            self.db_url,
            self.username,
            self.password,
            maxDegree=arguments.get("maxDegree"),
        )


class WeaklyConnectedComponentsHandler(AlgorithmHandler):
    def weakly_connected_components(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Weakly Connected Components parameters: {kwargs}")
            weakly_connected_components_result = gds.weakly_connected_components.stream(G, **kwargs)

        return weakly_connected_components_result
    
    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.weakly_connected_components(
            self.db_url,
            self.username,
            self.password,
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            seedProperty=arguments.get("seedProperty"),
            threshold=arguments.get("threshold"),
            consecutiveIds=arguments.get("consecutiveIds"),
            minComponentSize=arguments.get("minComponentSize"),
        )


class ApproximateMaximumKCutHandler(AlgorithmHandler):
    def approximate_maximum_k_cut(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Approximate Maximum K Cut parameters: {kwargs}")
            approximate_maximum_k_cut_result = gds.approximate_maximum_k_cut.stream(G, **kwargs)

        return approximate_maximum_k_cut_result
    
    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.approximate_maximum_k_cut(
            self.db_url,
            self.username,
            self.password,
            k=arguments.get("k"),
            iterations=arguments.get("iterations"),
            vnsMaxNeighborhoodOrder=arguments.get("vnsMaxNeighborhoodOrder"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )



class SpeakerListenerLabelPropagationHandler(AlgorithmHandler):
    def speaker_listener_label_propagation(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            logger.info(f"Speaker Listener Label Propagation parameters: {kwargs}")
            speaker_listener_label_propagation_result = gds.speaker_listener_label_propagation.stream(G, **kwargs)

        return speaker_listener_label_propagation_result
    
    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.speaker_listener_label_propagation(
            self.db_url,
            self.username,
            self.password,
            maxIterations=arguments.get("maxIterations"),
            minAssociationStrength=arguments.get("minAssociationStrength"),
            partitioning=arguments.get("partitioning"),
        )
