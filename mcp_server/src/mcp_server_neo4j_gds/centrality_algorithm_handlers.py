import logging
from typing import Any, Dict


from .algorithm_handler import AlgorithmHandler
from .gds import projected_graph

logger = logging.getLogger("mcp_server_neo4j_gds")


class ArticleRankHandler(AlgorithmHandler):
    def article_rank(self, **kwargs):
        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            args = locals()
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None
                and k not in ["nodes", "nodeIdentifierProperty", "sourceNodes"]
            }
            node_names = kwargs.get("nodes", None)
            node_identifier_property = kwargs.get("nodeIdentifierProperty")
            source_nodes = kwargs.get("sourceNodes", None)

            # Handle sourceNodes - convert names to IDs if nodeIdentifierProperty is provided
            if source_nodes is not None and node_identifier_property is not None:
                if isinstance(source_nodes, list):
                    # Handle list of source node names
                    query = f"""
                    UNWIND $names AS name
                    MATCH (s)
                    WHERE toLower(s.{node_identifier_property}) CONTAINS toLower(name)
                    RETURN id(s) as node_id
                    """
                    df = self.gds.run_cypher(
                        query,
                        params={
                            "names": source_nodes,
                        },
                    )
                    source_node_ids = df["node_id"].tolist()
                    params["sourceNodes"] = source_node_ids
                else:
                    # Handle single source node name
                    query = f"""
                    MATCH (s)
                    WHERE toLower(s.{node_identifier_property}) CONTAINS toLower($name)
                    RETURN id(s) as node_id
                    """
                    df = self.gds.run_cypher(
                        query,
                        params={
                            "name": source_nodes,
                        },
                    )
                    if not df.empty:
                        params["sourceNodes"] = int(df["node_id"].iloc[0])
            elif source_nodes is not None:
                # If sourceNodes provided but no nodeIdentifierProperty, pass through as-is
                params["sourceNodes"] = source_nodes

            logger.info(f"ArticleRank parameters: {params}")
            article_ranks = self.gds.articleRank.stream(G, **params)

        # Add node names to the results - extract the specified property
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in article_ranks["nodeId"]
            ]
            article_ranks["nodeName"] = node_name_values

        if node_names is not None:
            logger.info(f"Filtering ArticleRank results for nodes: {node_names}")
            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{node_identifier_property}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": node_names,
                },
            )
            node_ids = df["node_id"].tolist()
            article_ranks = article_ranks[article_ranks["nodeId"].isin(node_ids)]

        return article_ranks

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.article_rank(
            nodes=arguments.get("nodes"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            sourceNodes=arguments.get("sourceNodes"),
            scaler=arguments.get("scaler"),
            dampingFactor=arguments.get("dampingFactor"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
        )


class ArticulationPointsHandler(AlgorithmHandler):
    def articulation_points(self, **kwargs):
        with projected_graph(self.gds, undirected=True) as G:
            articulation_points = self.gds.articulationPoints.stream(G)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in articulation_points["nodeId"]
            ]
            articulation_points["nodeName"] = node_name_values

        return articulation_points

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.articulation_points(
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty")
        )


class BetweennessCentralityHandler(AlgorithmHandler):
    def betweenness_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodes", "nodeIdentifierProperty"]
            }
            logger.info(f"Betweenness centrality parameters: {params}")
            centrality = self.gds.betweenness.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in centrality["nodeId"]
            ]
            centrality["nodeName"] = node_name_values

        # Filter results by node names if provided
        node_names = kwargs.get("nodes", None)
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
            df = self.gds.run_cypher(
                query,
                params={
                    "names": node_names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.betweenness_centrality(
            nodes=arguments.get("nodes"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            samplingSize=arguments.get("samplingSize"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class BridgesHandler(AlgorithmHandler):
    def bridges(self, **kwargs):
        with projected_graph(self.gds, undirected=True) as G:
            bridges_result = self.gds.bridges.stream(G)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            from_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in bridges_result["from"]
            ]
            to_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in bridges_result["to"]
            ]
            bridges_result["fromName"] = from_name_values
            bridges_result["toName"] = to_name_values

        return bridges_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.bridges(
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty")
        )


class CELFHandler(AlgorithmHandler):
    def celf(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodeIdentifierProperty"]
            }
            logger.info(f"CELF parameters: {params}")
            result = self.gds.influenceMaximization.celf.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in result["nodeId"]
            ]
            result["nodeName"] = node_name_values

        return result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.celf(
            seedSetSize=arguments.get("seedSetSize"),
            monteCarloSimulations=arguments.get("monteCarloSimulations"),
            propagationProbability=arguments.get("propagationProbability"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class ClosenessCentralityHandler(AlgorithmHandler):
    def closeness_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodes", "nodeIdentifierProperty"]
            }
            logger.info(f"Closeness centrality parameters: {params}")
            centrality = self.gds.closeness.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in centrality["nodeId"]
            ]
            centrality["nodeName"] = node_name_values

        # Filter results by node names if provided
        node_names = kwargs.get("nodes", None)
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
            df = self.gds.run_cypher(
                query,
                params={
                    "names": node_names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.closeness_centrality(
            nodes=arguments.get("nodes"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            useWassermanFaust=arguments.get("useWassermanFaust"),
        )


class DegreeCentralityHandler(AlgorithmHandler):
    def degree_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            centrality = self.gds.degree.stream(G)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in centrality["nodeId"]
            ]
            centrality["nodeName"] = node_name_values

        # Filter results by node names if provided
        node_names = kwargs.get("nodes", None)
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
            df = self.gds.run_cypher(
                query,
                params={
                    "names": node_names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.degree_centrality(
            nodes=arguments.get("nodes"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class EigenvectorCentralityHandler(AlgorithmHandler):
    def eigenvector_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None
                and k not in ["nodes", "nodeIdentifierProperty", "sourceNodes"]
            }
            node_identifier_property = kwargs.get("nodeIdentifierProperty")
            source_nodes = kwargs.get("sourceNodes", None)

            # Handle sourceNodes - convert names to IDs if nodeIdentifierProperty is provided
            if source_nodes is not None and node_identifier_property is not None:
                if isinstance(source_nodes, list):
                    # Handle list of source node names
                    query = f"""
                    UNWIND $names AS name
                    MATCH (s)
                    WHERE toLower(s.{node_identifier_property}) CONTAINS toLower(name)
                    RETURN id(s) as node_id
                    """
                    df = self.gds.run_cypher(
                        query,
                        params={
                            "names": source_nodes,
                        },
                    )
                    source_node_ids = df["node_id"].tolist()
                    params["sourceNodes"] = source_node_ids
                else:
                    # Handle single source node name
                    query = f"""
                    MATCH (s)
                    WHERE toLower(s.{node_identifier_property}) CONTAINS toLower($name)
                    RETURN id(s) as node_id
                    """
                    df = self.gds.run_cypher(
                        query,
                        params={
                            "name": source_nodes,
                        },
                    )
                    if not df.empty:
                        params["sourceNodes"] = int(df["node_id"].iloc[0])
            elif source_nodes is not None:
                # If sourceNodes provided but no nodeIdentifierProperty, pass through as-is
                params["sourceNodes"] = source_nodes

            logger.info(f"Eigenvector centrality parameters: {params}")
            centrality = self.gds.eigenvector.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in centrality["nodeId"]
            ]
            centrality["nodeName"] = node_name_values

        # Filter results by node names if provided
        node_names = kwargs.get("nodes", None)
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
            df = self.gds.run_cypher(
                query,
                params={
                    "names": node_names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.eigenvector_centrality(
            nodes=arguments.get("nodes"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            sourceNodes=arguments.get("sourceNodes"),
            scaler=arguments.get("scaler"),
        )


class PageRankHandler(AlgorithmHandler):
    def pagerank(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None
                and k not in ["nodes", "nodeIdentifierProperty", "sourceNodes"]
            }
            node_identifier_property = kwargs.get("nodeIdentifierProperty")
            source_nodes = kwargs.get("sourceNodes", None)

            # Handle sourceNodes - convert names to IDs if nodeIdentifierProperty is provided
            if source_nodes is not None and node_identifier_property is not None:
                if isinstance(source_nodes, list):
                    # Handle list of source node names
                    query = f"""
                    UNWIND $names AS name
                    MATCH (s)
                    WHERE toLower(s.{node_identifier_property}) CONTAINS toLower(name)
                    RETURN id(s) as node_id
                    """
                    df = self.gds.run_cypher(
                        query,
                        params={
                            "names": source_nodes,
                        },
                    )
                    source_node_ids = df["node_id"].tolist()
                    params["sourceNodes"] = source_node_ids
                else:
                    # Handle single source node name
                    query = f"""
                    MATCH (s)
                    WHERE toLower(s.{node_identifier_property}) CONTAINS toLower($name)
                    RETURN id(s) as node_id
                    """
                    df = self.gds.run_cypher(
                        query,
                        params={
                            "name": source_nodes,
                        },
                    )
                    if not df.empty:
                        params["sourceNodes"] = int(df["node_id"].iloc[0])
            elif source_nodes is not None:
                # If sourceNodes provided but no nodeIdentifierProperty, pass through as-is
                params["sourceNodes"] = source_nodes

            logger.info(f"Pagerank parameters: {params}")
            pageranks = self.gds.pageRank.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in pageranks["nodeId"]
            ]
            pageranks["nodeName"] = node_name_values

        # Filter results by node names if provided
        node_names = kwargs.get("nodes", None)
        if node_names is not None:
            if node_identifier_property is None:
                raise ValueError(
                    "If 'nodes' is provided, 'nodeIdentifierProperty' must also be specified."
                )

            logger.info(f"Filtering pagerank results for nodes: {node_names}")
            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{node_identifier_property}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": node_names,
                },
            )
            node_ids = df["node_id"].tolist()
            pageranks = pageranks[pageranks["nodeId"].isin(node_ids)]

        return pageranks

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.pagerank(
            nodes=arguments.get("nodes"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            sourceNodes=arguments.get("sourceNodes"),
            dampingFactor=arguments.get("dampingFactor"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
        )


class HarmonicCentralityHandler(AlgorithmHandler):
    def harmonic_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            centrality = self.gds.closeness.harmonic.stream(G)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in centrality["nodeId"]
            ]
            centrality["nodeName"] = node_name_values

        # Filter results by node names if provided
        node_names = kwargs.get("nodes", None)
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
            df = self.gds.run_cypher(
                query,
                params={
                    "names": node_names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.harmonic_centrality(
            nodes=arguments.get("nodes"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
        )


class HITSHandler(AlgorithmHandler):
    def hits(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodes", "nodeIdentifierProperty"]
            }
            logger.info(f"HITS parameters: {params}")
            result = self.gds.hits.stream(G, **params)

        # Add node names to the results if nodeIdentifierProperty is provided
        node_identifier_property = kwargs.get("nodeIdentifierProperty")
        if node_identifier_property is not None:
            node_name_values = [
                self.gds.util.asNode(node_id).get(node_identifier_property)
                for node_id in result["nodeId"]
            ]
            result["nodeName"] = node_name_values

        # Filter results by node names if provided
        node_names = kwargs.get("nodes", None)
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
            df = self.gds.run_cypher(
                query,
                params={
                    "names": node_names,
                },
            )
            node_ids = df["node_id"].tolist()
            result = result[result["nodeId"].isin(node_ids)]

        return result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.hits(
            nodes=arguments.get("nodes"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            hitsIterations=arguments.get("hitsIterations"),
            authProperty=arguments.get("authProperty"),
            hubProperty=arguments.get("hubProperty"),
            partitioning=arguments.get("partitioning"),
        )
