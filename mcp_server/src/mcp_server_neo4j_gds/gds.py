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
        valid_properties = {}
        # loop over indices in rel_properties
        for i in range(len(rel_properties)):
            pi = gds.run_cypher(f"MATCH (n)-[r]-(m) RETURN distinct r.{rel_properties[i]} IS :: STRING AS ISSTRING")
            # check r0 dataframe has exactly one row and that row has False
            if pi.shape[0] == 1 and bool(pi['ISSTRING'][0]) is False:
                # add kv to dictionary valid_properties
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

def degree_centrality(db_url: str, username: str, password: str, **kwargs):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
    with projected_graph(gds) as G:
        centrality = gds.degree.stream(G)

    names = kwargs.get('names', None)
    if names is not None:
        query = """
        UNWIND $names AS name
        MATCH (s)
        WHERE toLower(s.name) CONTAINS toLower(name)
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

def pagerank(db_url: str, username: str, password: str, **kwargs):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
    with projected_graph(gds) as G:
        # If any optional parameter is not None, use that parameter
        args = locals()
        params = {k: v for k, v in kwargs.items() if v is not None and k not in ['names']}
        names = kwargs.get('names', None)
        logger.info(f"Pagerank parameters: {params}")
        pageranks = gds.pageRank.stream(G, **params)

    if names is not None:
        logger.info(f"Filtering pagerank results for nodes: {names}")
        query = """
        UNWIND $names AS name
        MATCH (s)
        WHERE toLower(s.name) CONTAINS toLower(name)
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

def find_shortest_path(db_url: str, username: str, password: str, start_node: str, end_node: str, **kwargs):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
    
    query = """
    MATCH (start)
    WHERE toLower(start.name) CONTAINS toLower($start_name)
    MATCH (end)
    WHERE toLower(end.name) CONTAINS toLower($end_name)
    RETURN id(start) as start_id, id(end) as end_id
    """
    
    df = gds.run_cypher(
        query,
        params={
            'start_name': start_node,
            'end_name': end_node
        }
    )
    
    if df.empty:
        return {
            "found": False,
            "message": "One or both node names not found"
        }
    
    start_node_id = int(df['start_id'].iloc[0])
    end_node_id = int(df['end_id'].iloc[0])

    with projected_graph(gds) as G:
        # If any optional parameter is not None, use that parameter
        args = locals()
        params = {k: v for k, v in kwargs.items() if v is not None}
        logger.info(f"Dijkstra single-source shortest path parameters: {params}")

        path_data = gds.shortestPath.dijkstra.stream(
            G,
            sourceNode=start_node_id,
            targetNode=end_node_id,
            **params
        )
    
        if path_data.empty:
            return {
                "found": False,
                "message": "No path found between the specified nodes"
            }
            
        # Convert to native Python types as needed - handle both list and Series objects
        node_ids = path_data['nodeIds'].iloc[0]
        costs = path_data['costs'].iloc[0]
        
        # Convert only if not already a list
        if hasattr(node_ids, 'tolist'):
            node_ids = node_ids.tolist()
        if hasattr(costs, 'tolist'):
            costs = costs.tolist()

        # Get node names using GDS utility function
        node_names = [gds.util.asNode(node_id) for node_id in node_ids]
            
        return {
            "totalCost": float(path_data['totalCost'].iloc[0]),
            "nodeIds": node_ids,
            "nodeNames": node_names,
            "path": path_data['path'].iloc[0],
            "costs": costs
        }
