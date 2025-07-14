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
                if v is not None and k not in ["nodes", "property_key"]
            }
            names = kwargs.get("nodes", None)
            logger.info(f"ArticleRank parameters: {params}")
            article_ranks = self.gds.articleRank.stream(G, **params)

        if names is not None:
            logger.info(f"Filtering ArticleRank results for nodes: {names}")
            property_key = kwargs.get("property_key", None)
            if property_key is None:
                raise ValueError(
                    "If 'nodes' is provided, 'property_key' must also be specified. "
                    "get_node_properties_keys should return all available property keys and the most appropriate one can be picked."
                )
            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": names,
                },
            )
            node_ids = df["node_id"].tolist()
            article_ranks = article_ranks[article_ranks["nodeId"].isin(node_ids)]

        return article_ranks

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.article_rank(
            nodes=arguments.get("nodes"),
            property_key=arguments.get("property_key"),
            sourceNodes=arguments.get("sourceNodes"),
            scaler=arguments.get("scaler"),
            dampingFactor=arguments.get("dampingFactor"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
        )


class ArticulationPointsHandler(AlgorithmHandler):
    def articulation_points(self):
        with projected_graph(self.gds) as G:
            articulation_points = self.gds.articulationPoints.stream(G)

        return articulation_points

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.articulation_points()


class BetweennessCentralityHandler(AlgorithmHandler):
    def betweenness_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            args = locals()
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodes", "property_key"]
            }
            names = kwargs.get("nodes", None)
            logger.info(f"Betweenness centrality parameters: {params}")
            centrality = self.gds.betweenness.stream(G, **params)

        names = kwargs.get("nodes", None)
        if names is not None:
            property_key = kwargs.get("property_key", None)
            if property_key is None:
                raise ValueError(
                    "If 'nodes' is provided, 'property_key' must also be specified. "
                    "get_node_properties_keys should return all available property keys and the most appropriate one can be picked."
                )

            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.betweenness_centrality(
            nodes=arguments.get("nodes"), property_key=arguments.get("property_key")
        )


class BridgesHandler(AlgorithmHandler):
    def bridges(self):
        with projected_graph(self.gds) as G:
            bridges_result = self.gds.bridges.stream(G)
        return bridges_result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.bridges()


class CELFHandler(AlgorithmHandler):
    def celf(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"CELF parameters: {params}")
            result = self.gds.influenceMaximization.celf.stream(G, **params)

        return result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.celf(
            seedSetSize=arguments.get("seedSetSize"),
            monteCarloSimulations=arguments.get("monteCarloSimulations"),
            propagationProbability=arguments.get("propagationProbability"),
        )


class ClosenessCentralityHandler(AlgorithmHandler):
    def closeness_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodes", "property_key"]
            }
            logger.info(f"Closeness centrality parameters: {params}")
            centrality = self.gds.closeness.stream(G, **params)

        names = kwargs.get("nodes", None)
        if names is not None:
            property_key = kwargs.get("property_key", None)
            if property_key is None:
                raise ValueError(
                    "If 'nodes' is provided, 'property_key' must also be specified. "
                    "get_node_properties_keys should return all available property keys and the most appropriate one can be picked."
                )

            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.closeness_centrality(
            nodes=arguments.get("nodes"), property_key=arguments.get("property_key")
        )


class DegreeCentralityHandler(AlgorithmHandler):
    def degree_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            centrality = self.gds.degree.stream(G)

        names = kwargs.get("nodes", None)
        if names is not None:
            property_key = kwargs.get("property_key", None)
            if property_key is None:
                raise ValueError(
                    "If 'nodes' is provided, 'property_key' must also be specified. "
                    "get_node_properties_keys should return all available property keys and the most appropriate one can be picked."
                )

            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.degree_centrality(
            nodes=arguments.get("nodes"), property_key=arguments.get("property_key")
        )


class EigenvectorCentralityHandler(AlgorithmHandler):
    def eigenvector_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodes", "property_key"]
            }
            logger.info(f"Eigenvector centrality parameters: {params}")
            centrality = self.gds.eigenvector.stream(G, **params)

        names = kwargs.get("nodes", None)
        if names is not None:
            property_key = kwargs.get("property_key", None)
            if property_key is None:
                raise ValueError(
                    "If 'nodes' is provided, 'property_key' must also be specified. "
                    "get_node_properties_keys should return all available property keys and the most appropriate one can be picked."
                )

            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.eigenvector_centrality(
            nodes=arguments.get("nodes"),
            property_key=arguments.get("property_key"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            sourceNodes=arguments.get("sourceNodes"),
            scaler=arguments.get("scaler"),
        )


class PageRankHandler(AlgorithmHandler):
    def pagerank(self, **kwargs):
        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            args = locals()
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodes", "property_key"]
            }
            names = kwargs.get("nodes", None)
            logger.info(f"Pagerank parameters: {params}")
            pageranks = self.gds.pageRank.stream(G, **params)

        if names is not None:
            logger.info(f"Filtering pagerank results for nodes: {names}")
            property_key = kwargs.get("property_key", None)
            if property_key is None:
                raise ValueError(
                    "If 'nodes' is provided, 'property_key' must also be specified. "
                    "get_node_properties_keys should return all available property keys and the most appropriate one can be picked."
                )
            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": names,
                },
            )
            node_ids = df["node_id"].tolist()
            pageranks = pageranks[pageranks["nodeId"].isin(node_ids)]

        return pageranks

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.pagerank(
            nodes=arguments.get("nodes"),
            property_key=arguments.get("property_key"),
            dampingFactor=arguments.get("dampingFactor"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance"),
        )


class HarmonicCentralityHandler(AlgorithmHandler):
    def harmonic_centrality(self, **kwargs):
        with projected_graph(self.gds) as G:
            centrality = self.gds.harmonic.stream(G)

        names = kwargs.get("nodes", None)
        if names is not None:
            property_key = kwargs.get("property_key", None)
            if property_key is None:
                raise ValueError(
                    "If 'nodes' is provided, 'property_key' must also be specified. "
                    "get_node_properties_keys should return all available property keys and the most appropriate one can be picked."
                )

            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": names,
                },
            )
            node_ids = df["node_id"].tolist()
            centrality = centrality[centrality["nodeId"].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.harmonic_centrality(
            nodes=arguments.get("nodes"), property_key=arguments.get("property_key")
        )


class HITSHandler(AlgorithmHandler):
    def hits(self, **kwargs):
        with projected_graph(self.gds) as G:
            params = {
                k: v
                for k, v in kwargs.items()
                if v is not None and k not in ["nodes", "property_key"]
            }
            logger.info(f"HITS parameters: {params}")
            result = self.gds.hits.stream(G, **params)

        names = kwargs.get("nodes", None)
        if names is not None:
            property_key = kwargs.get("property_key", None)
            if property_key is None:
                raise ValueError(
                    "If 'nodes' is provided, 'property_key' must also be specified. "
                    "get_node_properties_keys should return all available property keys and the most appropriate one can be picked."
                )

            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = self.gds.run_cypher(
                query,
                params={
                    "names": names,
                },
            )
            node_ids = df["node_id"].tolist()
            result = result[result["nodeId"].isin(node_ids)]

        return result

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.hits(
            nodes=arguments.get("nodes"),
            property_key=arguments.get("property_key"),
            hitsIterations=arguments.get("hitsIterations"),
            authProperty=arguments.get("authProperty"),
            hubProperty=arguments.get("hubProperty"),
            partitioning=arguments.get("partitioning"),
        )
