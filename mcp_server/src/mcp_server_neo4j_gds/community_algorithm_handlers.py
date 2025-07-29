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
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodeIdentifierProperty"]
            }
            logger.info(f"HDBSCAN parameters: {params}")
            hdbscan_result = self.gds.hdbscan.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in hdbscan_result["nodeId"]
            ]
            hdbscan_result["nodeName"] = node_name_values

        return hdbscan_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.hdbscan(
            nodeProperty=arguments.get("nodeProperty"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            minClusterSize=arguments.get("minClusterSize"),
            samples=arguments.get("samples"),
            leafSize=arguments.get("leafSize"),
        )


class KCoreDecompositionHandler(AlgorithmHandler):
    def k_core_decomposition(self, **kwargs):
        with projected_graph(self.gds, undirected=True) as G:
            logger.info("Running K-Core Decomposition")
            kcore_decomposition_result = self.gds.kcore.stream(G)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in kcore_decomposition_result["nodeId"]
            ]
            kcore_decomposition_result["nodeName"] = node_name_values

        return kcore_decomposition_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_core_decomposition(
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty")
        )


class K1ColoringHandler(AlgorithmHandler):
    def k_1_coloring(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodeIdentifierProperty"]
            }
            logger.info(f"K-1 Coloring parameters: {params}")
            k1_coloring_result = self.gds.k1coloring.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in k1_coloring_result["nodeId"]
            ]
            k1_coloring_result["nodeName"] = node_name_values

        return k1_coloring_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_1_coloring(
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            maxIterations=arguments.get("maxIterations"),
            minCommunitySize=arguments.get("minCommunitySize"),
        )


class KMeansClusteringHandler(AlgorithmHandler):
    def k_means_clustering(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodeIdentifierProperty"]
            }
            logger.info(f"K-Means Clustering parameters: {params}")
            kmeans_clustering_result = self.gds.kmeans.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in kmeans_clustering_result["nodeId"]
            ]
            kmeans_clustering_result["nodeName"] = node_name_values

        return kmeans_clustering_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.k_means_clustering(
            nodeProperty=arguments.get("nodeProperty"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
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
        # Filter out nodeIdentifierProperty as it's not a GDS algorithm parameter
        gds_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["nodeIdentifierProperty"]
        }

        with projected_graph(self.gds) as G:
            logger.info(f"Label Propagation parameters: {gds_kwargs}")
            label_propagation_result = self.gds.labelPropagation.stream(G, **gds_kwargs)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in label_propagation_result["nodeId"]
            ]
            label_propagation_result["nodeName"] = node_name_values

        return label_propagation_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.label_propagation(
            maxIterations=arguments.get("maxIterations"),
            nodeWeightProperty=arguments.get("nodeWeightProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            seedProperty=arguments.get("seedProperty"),
            consecutiveIds=arguments.get("consecutiveIds"),
            minCommunitySize=arguments.get("minCommunitySize"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class LeidenHandler(AlgorithmHandler):
    def leiden(self, **kwargs):
        # Filter out nodeIdentifierProperty as it's not a GDS algorithm parameter
        gds_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["nodeIdentifierProperty"]
        }

        with projected_graph(self.gds, undirected=True) as G:
            logger.info(f"Leiden parameters: {gds_kwargs}")
            leiden_result = self.gds.leiden.stream(G, **gds_kwargs)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in leiden_result["nodeId"]
            ]
            leiden_result["nodeName"] = node_name_values

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
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class LocalClusteringCoefficientHandler(AlgorithmHandler):
    def local_clustering_coefficient(self, **kwargs):
        # Filter out non-GDS algorithm parameters
        gds_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in ["nodeIdentifierProperty", "nodes"]
        }

        with projected_graph(self.gds, undirected=True) as G:
            logger.info(f"Local Clustering Coefficient parameters: {gds_kwargs}")
            local_clustering_coefficient_result = (
                self.gds.localClusteringCoefficient.stream(G, **gds_kwargs)
            )

        # Get filtering parameters
        node_names = kwargs.get("nodes", None)
        node_identifier_property = kwargs.get("nodeIdentifierProperty")

        # Add node names to the results if nodeIdentifierProperty is provided
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in local_clustering_coefficient_result["nodeId"]
            ]
            local_clustering_coefficient_result["nodeName"] = node_name_values

        # Filter results if nodes parameter provided
        if node_names is not None:
            if node_identifier_property is None:
                raise ValueError(
                    "If 'nodes' is provided, 'nodeIdentifierProperty' must also be specified."
                )

            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{node_identifier_property}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(query, params={"names": node_names})
            node_ids = df["node_id"].tolist()
            local_clustering_coefficient_result = local_clustering_coefficient_result[
                local_clustering_coefficient_result["nodeId"].isin(node_ids)
            ]

        return local_clustering_coefficient_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.local_clustering_coefficient(
            triangleCountProperty=arguments.get("triangleCountProperty"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            nodes=arguments.get("nodes"),
        )


class LouvainHandler(AlgorithmHandler):
    def louvain(self, **kwargs):
        # Filter out nodeIdentifierProperty as it's not a GDS algorithm parameter
        gds_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["nodeIdentifierProperty"]
        }

        with projected_graph(self.gds) as G:
            logger.info(f"Louvain parameters: {gds_kwargs}")
            louvain_result = self.gds.louvain.stream(G, **gds_kwargs)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in louvain_result["nodeId"]
            ]
            louvain_result["nodeName"] = node_name_values

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
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class ModularityMetricHandler(AlgorithmHandler):
    def modularity_metric(self, **kwargs):
        with projected_graph(self.gds) as G:
            logger.info(f"Modularity Metric parameters: {kwargs}")
            modularity_metric_result = self.gds.modularity.stream(G, **kwargs)

        return modularity_metric_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.modularity_metric(
            communityProperty=arguments.get("communityProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class ModularityOptimizationHandler(AlgorithmHandler):
    def modularity_optimization(self, **kwargs):
        # Filter out nodeIdentifierProperty as it's not a GDS algorithm parameter
        gds_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["nodeIdentifierProperty"]
        }

        with projected_graph(self.gds) as G:
            logger.info(f"Modularity Optimization parameters: {gds_kwargs}")
            modularity_optimization_result = self.gds.modularityOptimization.stream(
                G, **gds_kwargs
            )

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in modularity_optimization_result["nodeId"]
            ]
            modularity_optimization_result["nodeName"] = node_name_values

        return modularity_optimization_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.modularity_optimization(
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
            seedProperty=arguments.get("seedProperty"),
            consecutiveIds=arguments.get("consecutiveIds"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            minCommunitySize=arguments.get("minCommunitySize"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class StronglyConnectedComponentsHandler(AlgorithmHandler):
    def strongly_connected_components(self, **kwargs):
        # Filter out nodeIdentifierProperty as it's not a GDS algorithm parameter
        gds_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["nodeIdentifierProperty"]
        }

        with projected_graph(self.gds) as G:
            logger.info(f"Strongly Connected Components parameters: {gds_kwargs}")
            strongly_connected_components_result = self.gds.scc.stream(G, **gds_kwargs)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in strongly_connected_components_result["nodeId"]
            ]
            strongly_connected_components_result["nodeName"] = node_name_values

        return strongly_connected_components_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.strongly_connected_components(
            consecutiveIds=arguments.get("consecutiveIds"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class TriangleCountHandler(AlgorithmHandler):
    def triangle_count(self, **kwargs):
        # Filter out non-GDS algorithm parameters
        gds_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in ["nodeIdentifierProperty", "nodes"]
        }

        with projected_graph(self.gds, undirected=True) as G:
            logger.info(f"Triangle Count parameters: {gds_kwargs}")
            triangle_count_result = self.gds.triangleCount.stream(G, **gds_kwargs)

        # Get filtering parameters
        node_names = kwargs.get("nodes", None)
        node_identifier_property = kwargs.get("nodeIdentifierProperty")

        # Add node names to the results if nodeIdentifierProperty is provided
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in triangle_count_result["nodeId"]
            ]
            triangle_count_result["nodeName"] = node_name_values

        # Filter results if nodes parameter provided
        if node_names is not None:
            if node_identifier_property is None:
                raise ValueError(
                    "If 'nodes' is provided, 'nodeIdentifierProperty' must also be specified."
                )

            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{node_identifier_property}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(query, params={"names": node_names})
            node_ids = df["node_id"].tolist()
            triangle_count_result = triangle_count_result[
                triangle_count_result["nodeId"].isin(node_ids)
            ]

        return triangle_count_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.triangle_count(
            maxDegree=arguments.get("maxDegree"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            nodes=arguments.get("nodes"),
        )


class WeaklyConnectedComponentsHandler(AlgorithmHandler):
    def weakly_connected_components(self, **kwargs):
        # Filter out nodeIdentifierProperty as it's not a GDS algorithm parameter
        gds_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["nodeIdentifierProperty"]
        }

        with projected_graph(self.gds) as G:
            logger.info(f"Weakly Connected Components parameters: {gds_kwargs}")
            weakly_connected_components_result = self.gds.wcc.stream(G, **gds_kwargs)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in weakly_connected_components_result["nodeId"]
            ]
            weakly_connected_components_result["nodeName"] = node_name_values

        return weakly_connected_components_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.weakly_connected_components(
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            seedProperty=arguments.get("seedProperty"),
            threshold=arguments.get("threshold"),
            consecutiveIds=arguments.get("consecutiveIds"),
            minComponentSize=arguments.get("minComponentSize"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class ApproximateMaximumKCutHandler(AlgorithmHandler):
    def approximate_maximum_k_cut(self, **kwargs):
        # Filter out nodeIdentifierProperty as it's not a GDS algorithm parameter
        gds_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["nodeIdentifierProperty"]
        }

        with projected_graph(self.gds) as G:
            logger.info(f"Approximate Maximum K Cut parameters: {gds_kwargs}")
            approximate_maximum_k_cut_result = self.gds.maxkcut.stream(G, **gds_kwargs)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in approximate_maximum_k_cut_result["nodeId"]
            ]
            approximate_maximum_k_cut_result["nodeName"] = node_name_values

        return approximate_maximum_k_cut_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.approximate_maximum_k_cut(
            k=arguments.get("k"),
            iterations=arguments.get("iterations"),
            vnsMaxNeighborhoodOrder=arguments.get("vnsMaxNeighborhoodOrder"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            minCommunitySize=arguments.get("minCommunitySize"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class SpeakerListenerLabelPropagationHandler(AlgorithmHandler):
    def speaker_listener_label_propagation(self, **kwargs):
        # Filter out nodeIdentifierProperty as it's not a GDS algorithm parameter
        gds_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["nodeIdentifierProperty"]
        }

        with projected_graph(self.gds) as G:
            logger.info(f"Speaker Listener Label Propagation parameters: {gds_kwargs}")
            speaker_listener_label_propagation_result = self.gds.sllpa.stream(
                G, **gds_kwargs
            )

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in speaker_listener_label_propagation_result["nodeId"]
            ]
            speaker_listener_label_propagation_result["nodeName"] = node_name_values

        return speaker_listener_label_propagation_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.speaker_listener_label_propagation(
            maxIterations=arguments.get("maxIterations"),
            minAssociationStrength=arguments.get("minAssociationStrength"),
            partitioning=arguments.get("partitioning"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )
