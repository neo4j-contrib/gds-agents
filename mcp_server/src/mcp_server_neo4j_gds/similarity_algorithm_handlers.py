import logging
from typing import Dict, Any

from graphdatascience import GraphDataScience

from .algorithm_handler import AlgorithmHandler
from .gds import projected_graph

logger = logging.getLogger("mcp_server_neo4j_gds")


class NodeSimilarityHandler(AlgorithmHandler):
    def node_similarity(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodeIdentifierProperty"]
            }
            logger.info(f"Node Similarity parameters: {params}")
            node_similarity_result = self.gds.nodeSimilarity.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node1_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in node_similarity_result["node1"]
            ]
            node2_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in node_similarity_result["node2"]
            ]
            node_similarity_result["node1Name"] = node1_name_values
            node_similarity_result["node2Name"] = node2_name_values

        return node_similarity_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.node_similarity(
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
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
    def handle_input_nodes(
        self,
        input_nodes,
        input_nodes_variable_name,
        node_identifier_property,
        call_params,
    ):
        # Handle input nodes - convert names to IDs if nodeIdentifierProperty is provided
        if input_nodes is not None and node_identifier_property is not None:
            if isinstance(input_nodes, list):
                # Handle list of node names
                query = f"""
                    UNWIND $names AS name
                    MATCH (s)
                    WHERE toLower(s.{node_identifier_property}) CONTAINS toLower(name)
                    RETURN id(s) as node_id
                    """
                df = self.gds.run_cypher(
                    query,
                    params={
                        "names": input_nodes,
                    },
                )
                input_node_ids = df["node_id"].tolist()
                call_params[input_nodes_variable_name] = input_node_ids
            else:
                # Handle single  node name
                query = f"""
                    MATCH (s)
                    WHERE toLower(s.{node_identifier_property}) CONTAINS toLower($name)
                    RETURN id(s) as node_id
                    """
                df = self.gds.run_cypher(
                    query,
                    params={
                        "name": input_nodes,
                    },
                )
                if not df.empty:
                    call_params[input_nodes_variable_name] = int(df["node_id"].iloc[0])
        elif input_nodes is not None:
            # If input_nodes provided but no nodeIdentifierProperty, pass through as-is
            call_params[input_nodes_variable_name] = input_nodes

    def filtered_node_similarity(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None
                and k
                not in [
                    "nodeIdentifierProperty",
                    "sourceNodeFilter",
                    "targetNodeFilter",
                ]
            }
            node_identifier_property = kwargs.get("nodeIdentifierProperty")
            source_nodes = kwargs.get("sourceNodeFilter", None)
            target_nodes = kwargs.get("targetNodeFilter", None)
            self.handle_input_nodes(
                source_nodes, "sourceNodeFilter", node_identifier_property, params
            )
            self.handle_input_nodes(
                target_nodes, "targetNodeFilter", node_identifier_property, params
            )
            logger.info(f"Filtered Node Similarity parameters: {params}")
            filtered_node_similarity_result = self.gds.nodeSimilarity.filtered.stream(
                G, **params
            )

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node1_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in filtered_node_similarity_result["node1"]
            ]
            node2_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in filtered_node_similarity_result["node2"]
            ]
            filtered_node_similarity_result["node1Name"] = node1_name_values
            filtered_node_similarity_result["node2Name"] = node2_name_values

        return filtered_node_similarity_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.filtered_node_similarity(
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
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
