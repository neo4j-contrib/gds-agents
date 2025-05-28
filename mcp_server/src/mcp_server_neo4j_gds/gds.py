from graphdatascience import GraphDataScience
import uuid
from contextlib import contextmanager
import logging


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
def projected_graph(gds):
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

def count_nodes(db_url: str, username: str, password: str):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
    with projected_graph(gds) as G:
        return G.node_count()

def get_node_properties_keys(db_url: str, username: str, password: str):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
    with projected_graph(gds) as G:
        query = """
        MATCH (n)
        RETURN DISTINCT keys(properties(n)) AS properties_keys
        """
        df = gds.run_cypher(query)
        if df.empty:
            return []
        return df['properties_keys'].iloc[0]
