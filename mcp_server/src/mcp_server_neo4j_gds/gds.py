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
def projected_graph(gds, relationship_property: str = "distance"):
    graph_name = f"temp_graph_{uuid.uuid4().hex[:8]}"
    try:
        G, _ = gds.graph.cypher.project(
            """
            MATCH (n)-[r]-(m)
            WITH n, r, m
            RETURN gds.graph.project(
                $graph_name,
                n,
                m,
                {
                sourceNodeLabels: labels(n),
                targetNodeLabels: labels(m),
                relationshipType: type(r),
                relationshipProperties: { weight: r[$relationship_property] }
            }  
            )
            """,
            graph_name=graph_name,
            relationship_property=relationship_property
        )
        yield G
    finally:
        gds.graph.drop(graph_name)

def count_nodes(db_url: str, username: str, password: str, relationship_property: str):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
    with projected_graph(gds, relationship_property) as G:
        return G.node_count()

def degree_centrality(db_url: str, username: str, password: str, **kwargs):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
    with projected_graph(gds) as G:
        centrality = gds.degree.stream(G)

    stations = kwargs.get('stations', None)
    if stations is not None:
        query = """
        UNWIND $stations AS station
        MATCH (s:UndergroundStation)
        WHERE toLower(s.name) CONTAINS toLower(station)
        RETURN id(s) as node_id
        """
        df = gds.run_cypher(
            query,
            params={
                'stations': stations,
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
        params = {k: v for k, v in kwargs.items() if v is not None and k not in ['stations']}
        stations = kwargs.get('stations', None)
        logger.info(f"Pagerank parameters: {params}")
        pageranks = gds.pageRank.stream(G, **params)

    if stations is not None:
        logger.info(f"Filtering pagerank results for stations: {stations}")
        query = """
        UNWIND $stations AS station
        MATCH (s:UndergroundStation)
        WHERE toLower(s.name) CONTAINS toLower(station)
        RETURN id(s) as node_id
        """
        df = gds.run_cypher(
            query,
            params={
                'stations': stations,
            }
        )
        node_ids = df['node_id'].tolist()
        pageranks = pageranks[pageranks['nodeId'].isin(node_ids)]

    return pageranks

def find_shortest_path(db_url: str, username: str, password: str, start_station: str, end_station: str, relationship_property: str):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)
    
    query = """
    MATCH (start:UndergroundStation)
    WHERE toLower(start.name) CONTAINS toLower($start_name)
    MATCH (end:UndergroundStation)
    WHERE toLower(end.name) CONTAINS toLower($end_name)
    RETURN id(start) as start_id, id(end) as end_id
    """
    
    df = gds.run_cypher(
        query,
        params={
            'start_name': start_station,
            'end_name': end_station
        }
    )
    
    if df.empty:
        return {
            "found": False,
            "message": "One or both station names not found"
        }
    
    start_node_id = int(df['start_id'].iloc[0])
    end_node_id = int(df['end_id'].iloc[0])

    with projected_graph(gds) as G:
        path_data = gds.shortestPath.dijkstra.stream(
            G,
            sourceNode=start_node_id,
            targetNode=end_node_id,
            relationshipTypes=["LINK"],
            relationshipWeightProperty="weight"
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

        # Get station names using GDS utility function
        station_names = [gds.util.asNode(node_id) for node_id in node_ids]
            
        return {
            "totalCost": float(path_data['totalCost'].iloc[0]),
            "nodeIds": node_ids,
            "stationNames": station_names,
            "path": path_data['path'].iloc[0],
            "costs": costs
        }
