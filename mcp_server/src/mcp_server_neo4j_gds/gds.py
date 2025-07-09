from graphdatascience import GraphDataScience
import uuid
from contextlib import contextmanager
import logging

"""
Graph Data Science (GDS) utilities for Neo4j.

This module provides graph projection functionality that supports both directed and undirected graphs.
Some algorithms work better or are specifically designed for undirected graphs:

Algorithms that use UNDIRECTED graphs:
- Betweenness Centrality (better results on undirected graphs)
- Louvain Community Detection
- Leiden Community Detection  
- Label Propagation
- Local Clustering Coefficient
- Minimum Weight Spanning Tree
- K-Spanning Tree

Algorithms that use DIRECTED graphs (default):
- PageRank
- ArticleRank
- HITS
- Dijkstra Shortest Path
- Most other path algorithms
- Most centrality algorithms

The projected_graph function now accepts an 'undirected' parameter to control graph orientation.
"""

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_server_neo4j_gds.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('mcp_server_neo4j_gds')

@contextmanager
def projected_graph(gds, undirected=False):
    """
    Project a graph from the database.
    
    Args:
        gds: GraphDataScience instance
        undirected: If True, project as undirected graph. Default is False (directed).
    """
    graph_name = f"temp_graph_{uuid.uuid4().hex[:8]}"
    try:
        rel_properties = gds.run_cypher("MATCH (n)-[r]-(m) RETURN DISTINCT keys(properties(r))")['keys(properties(r))'][0]
        # Include all properties that are not STRING
        valid_properties = {}
        for i in range(len(rel_properties)):
            pi = gds.run_cypher(f"MATCH (n)-[r]-(m) RETURN distinct r.{rel_properties[i]} IS :: STRING AS ISSTRING")
            if pi.shape[0] == 1 and bool(pi['ISSTRING'][0]) is False:
                valid_properties[rel_properties[i]] = f"r.{rel_properties[i]}"
        prop_map = ", ".join(f"{prop}: r.{prop}" for prop in valid_properties)

        # Configure graph projection based on undirected parameter
        if undirected:
            # For undirected graphs, use undirectedRelationshipTypes: ['*'] to make all relationships undirected
            G, _ = gds.graph.cypher.project(
                f"""
                       MATCH (n)-[r]-(m)
                       WITH n, r, m
                       RETURN gds.graph.project(
                           $graph_name,
                           n,
                           m,
                           {{
                           sourceNodeLabels: labels(n),
                           targetNodeLabels: labels(m),
                           relationshipType: type(r),
                           relationshipProperties: {{{prop_map}}},
                           undirectedRelationshipTypes: ['*']
                       }}
                       )
                       """,
                graph_name=graph_name
            )
        else:
            # Default directed projection
            G, _ = gds.graph.cypher.project(
                f"""
                       MATCH (n)-[r]-(m)
                       WITH n, r, m
                       RETURN gds.graph.project(
                           $graph_name,
                           n,
                           m,
                           {{
                           sourceNodeLabels: labels(n),
                           targetNodeLabels: labels(m),
                           relationshipType: type(r),
                           relationshipProperties: {{{prop_map}}}
                       }}
                       )
                       """,
                graph_name=graph_name
            )
        yield G
    finally:
        gds.graph.drop(graph_name)

def count_nodes(gds: GraphDataScience):
    with projected_graph(gds) as G:
        return G.node_count()

def get_node_properties_keys(gds: GraphDataScience):
    with projected_graph(gds) as G:
        query = """
        MATCH (n)
        RETURN DISTINCT keys(properties(n)) AS properties_keys
        """
        df = gds.run_cypher(query)
        if df.empty:
            return []
        return df['properties_keys'].iloc[0]
