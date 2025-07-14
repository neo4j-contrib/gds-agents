import logging
from typing import Dict, Any


from .algorithm_handler import AlgorithmHandler
from .gds import projected_graph

logger = logging.getLogger("mcp_server_neo4j_gds")


class ConductanceHandler(AlgorithmHandler):
    def conductance(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Conductance parameters: {kwargs}")
            conductance = self.gds.conductance.stream(G, **kwargs)

        return conductance

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.conductance(
            communityProperty=arguments.get("communityProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class HDBSCANHandler(AlgorithmHandler):
    def hdbscan(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"HDBSCAN parameters: {kwargs}")
            hdbscan_result = self.gds.hdbscan.stream(G, **kwargs)

        return hdbscan_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.hdbscan(
            nodeProperty=arguments.get("nodeProperty"),
            minClusterSize=arguments.get("minClusterSize"),
            samples=arguments.get("samples"),
            leafSize=arguments.get("leafSize"),
        )


class KCoreDecompositionHandler(AlgorithmHandler):
    def k_core_decomposition(self):
        with projected_graph(self.gds, undirected=True) as G:
            logger.info("Running K-Core Decomposition")
            kcore_decomposition_result = self.gds.kcore_decomposition.stream(G)

        return kcore_decomposition_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_core_decomposition()


class K1ColoringHandler(AlgorithmHandler):
    def k_1_coloring(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"K-1 Coloring parameters: {kwargs}")
            k1_coloring_result = self.gds.k1_coloring.stream(G, **kwargs)

        return k1_coloring_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_1_coloring(
            maxIterations=arguments.get("maxIterations"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )


class KMeansClusteringHandler(AlgorithmHandler):
    def k_means_clustering(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"K-Means Clustering parameters: {kwargs}")
            kmeans_clustering_result = self.gds.kmeans_clustering.stream(G, **kwargs)

        return kmeans_clustering_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_means_clustering(
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
    def label_propagation(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Label Propagation parameters: {kwargs}")
            label_propagation_result = self.gds.label_propagation.stream(G, **kwargs)

        return label_propagation_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.label_propagation(
            maxIterations=arguments.get("maxIterations"),
            nodeWeightProperty=arguments.get("nodeWeightProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            seedProperty=arguments.get("seedProperty"),
            consecutiveIds=arguments.get("consecutiveIds"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )


class LeidenHandler(AlgorithmHandler):
    def leiden(self, **kwargs):
        with projected_graph(self.gds, undirected=True) as G:
            logger.info(f"Leiden parameters: {kwargs}")
            leiden_result = self.gds.leiden.stream(G, **kwargs)

        return leiden_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.leiden(
            maxLevels=arguments.get("maxLevels"),
            gamma=arguments.get("gamma"),
            theta=arguments.get("theta"),
            tolerance=arguments.get("tolerance"),
            includeIntermediateCommunities=arguments.get(
                "includeIntermediateCommunities"
            ),
            seedProperty=arguments.get("seedProperty"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )


class LocalClusteringCoefficientHandler(AlgorithmHandler):
    def local_clustering_coefficient(self, **kwargs):
        with projected_graph(self.gds, undirected=True) as G:
            logger.info(f"Local Clustering Coefficient parameters: {kwargs}")
            local_clustering_coefficient_result = (
                self.gds.local_clustering_coefficient.stream(G, **kwargs)
            )

        return local_clustering_coefficient_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.local_clustering_coefficient(
            triangleCountProperty=arguments.get("triangleCountProperty"),
        )


class LouvainHandler(AlgorithmHandler):
    def louvain(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Louvain parameters: {kwargs}")
            louvain_result = self.gds.louvain.stream(G, **kwargs)

        return louvain_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.louvain(
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            seedProperty=arguments.get("seedProperty"),
            maxLevels=arguments.get("maxLevels"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
            includeIntermediateCommunities=arguments.get(
                "includeIntermediateCommunities"
            ),
            consecutiveIds=arguments.get("consecutiveIds"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )


class ModularityMetricHandler(AlgorithmHandler):
    def modularity_metric(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Modularity Metric parameters: {kwargs}")
            modularity_metric_result = self.gds.modularity_metric.stream(G, **kwargs)

        return modularity_metric_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.modularity_metric(
            communityProperty=arguments.get("communityProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class ModularityOptimizationHandler(AlgorithmHandler):
    def modularity_optimization(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Modularity Optimization parameters: {kwargs}")
            modularity_optimization_result = self.gds.modularity_optimization.stream(
                G, **kwargs
            )

        return modularity_optimization_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.modularity_optimization(
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
            seedProperty=arguments.get("seedProperty"),
            consecutiveIds=arguments.get("consecutiveIds"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )


class StronglyConnectedComponentsHandler(AlgorithmHandler):
    def strongly_connected_components(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Strongly Connected Components parameters: {kwargs}")
            strongly_connected_components_result = (
                self.gds.strongly_connected_components.stream(G, **kwargs)
            )

        return strongly_connected_components_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.strongly_connected_components(
            consecutiveIds=arguments.get("consecutiveIds"),
        )


class TriangleCountHandler(AlgorithmHandler):
    def triangle_count(self, **kwargs):
        with projected_graph(self.gds, undirected=True) as G:
            logger.info(f"Triangle Count parameters: {kwargs}")
            triangle_count_result = self.gds.triangle_count.stream(G, **kwargs)

        return triangle_count_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.triangle_count(
            maxDegree=arguments.get("maxDegree"),
        )


class WeaklyConnectedComponentsHandler(AlgorithmHandler):
    def weakly_connected_components(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Weakly Connected Components parameters: {kwargs}")
            weakly_connected_components_result = (
                self.gds.weakly_connected_components.stream(G, **kwargs)
            )

        return weakly_connected_components_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.weakly_connected_components(
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            seedProperty=arguments.get("seedProperty"),
            threshold=arguments.get("threshold"),
            consecutiveIds=arguments.get("consecutiveIds"),
            minComponentSize=arguments.get("minComponentSize"),
        )


class ApproximateMaximumKCutHandler(AlgorithmHandler):
    def approximate_maximum_k_cut(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Approximate Maximum K Cut parameters: {kwargs}")
            approximate_maximum_k_cut_result = (
                self.gds.approximate_maximum_k_cut.stream(G, **kwargs)
            )

        return approximate_maximum_k_cut_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.approximate_maximum_k_cut(
            k=arguments.get("k"),
            iterations=arguments.get("iterations"),
            vnsMaxNeighborhoodOrder=arguments.get("vnsMaxNeighborhoodOrder"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )


class SpeakerListenerLabelPropagationHandler(AlgorithmHandler):
    def speaker_listener_label_propagation(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Speaker Listener Label Propagation parameters: {kwargs}")
            speaker_listener_label_propagation_result = (
                self.gds.speaker_listener_label_propagation.stream(G, **kwargs)
            )

        return speaker_listener_label_propagation_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.speaker_listener_label_propagation(
            maxIterations=arguments.get("maxIterations"),
            minAssociationStrength=arguments.get("minAssociationStrength"),
            partitioning=arguments.get("partitioning"),
        )
