import logging
from typing import Any, Dict

from graphdatascience import GraphDataScience

from .algorithm_handler import AlgorithmHandler
from .gds import projected_graph


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_server_neo4j_gds.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('mcp_server_neo4j_gds')

class ArticleRankHandler(AlgorithmHandler):
    def article_rank(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            # If any optional parameter is not None, use that parameter
            args = locals()
            params = {k: v for k, v in kwargs.items() if v is not None and k not in ['nodes', 'property_key']}
            names = kwargs.get('nodes', None)
            logger.info(f"ArticleRank parameters: {params}")
            article_ranks = gds.articleRank.stream(G, **params)

        if names is not None:
            logger.info(f"Filtering ArticleRank results for nodes: {names}")
            property_key = kwargs.get('property_key', None)
            if property_key is None:
                raise ValueError("If 'nodes' is provided, 'property_key' must also be specified. "
                                 "get_node_properties_keys should return all available property keys and the most appropriate one can be picked.")
            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = gds.run_cypher(
                query,
                params={
                    'names': names,
                }
            )
            node_ids = df['node_id'].tolist()
            article_ranks = article_ranks[article_ranks['nodeId'].isin(node_ids)]

        return article_ranks

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.article_rank(
            self.db_url,
            self.username,
            self.password,
            nodes=arguments.get("nodes"),
            property_key=arguments.get("property_key"),
            sourceNodes=arguments.get("sourceNodes"),
            scaler=arguments.get("scaler"),
            dampingFactor=arguments.get("dampingFactor"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance")
        )


class DegreeCentralityHandler(AlgorithmHandler):
    def degree_centrality(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            centrality = gds.degree.stream(G)

        names = kwargs.get('nodes', None)
        if names is not None:
            property_key = kwargs.get('property_key', None)
            if property_key is None:
                raise ValueError("If 'nodes' is provided, 'property_key' must also be specified. "
                                 "get_node_properties_keys should return all available property keys and the most appropriate one can be picked.")

            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = gds.run_cypher(
                query,
                params={
                    'names': names,
                }
            )
            node_ids = df['node_id'].tolist()
            centrality = centrality[centrality['nodeId'].isin(node_ids)]

        return centrality

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.degree_centrality(
            self.db_url,
            self.username,
            self.password,
            nodes=arguments.get("nodes"),
            property_key=arguments.get("property_key")
        )


class PageRankHandler(AlgorithmHandler):
    def pagerank(self, db_url: str, username: str, password: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
        with projected_graph(gds) as G:
            # If any optional parameter is not None, use that parameter
            args = locals()
            params = {k: v for k, v in kwargs.items() if v is not None and k not in ['nodes', 'property_key']}
            names = kwargs.get('nodes', None)
            logger.info(f"Pagerank parameters: {params}")
            pageranks = gds.pageRank.stream(G, **params)

        if names is not None:
            logger.info(f"Filtering pagerank results for nodes: {names}")
            property_key = kwargs.get('property_key', None)
            if property_key is None:
                raise ValueError("If 'nodes' is provided, 'property_key' must also be specified. "
                                 "get_node_properties_keys should return all available property keys and the most appropriate one can be picked.")
            query = f"""
            UNWIND $names AS name
            MATCH (s)
            WHERE toLower(s.{property_key}) CONTAINS toLower(name)
            RETURN id(s) as node_id
            """
            df = gds.run_cypher(
                query,
                params={
                    'names': names,
                }
            )
            node_ids = df['node_id'].tolist()
            pageranks = pageranks[pageranks['nodeId'].isin(node_ids)]

        return pageranks

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.pagerank(
            self.db_url,
            self.username,
            self.password,
            nodes=arguments.get("nodes"),
            property_key=arguments.get("property_key"),
            dampingFactor=arguments.get("dampingFactor"),
            maxIterations=arguments.get("maxIterations"),
            tolerance=arguments.get("tolerance")
        )
