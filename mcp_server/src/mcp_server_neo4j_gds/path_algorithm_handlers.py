import logging
from typing import Dict, Any

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

class DijkstraShortestPathHandler(AlgorithmHandler):
    def find_shortest_path(self, db_url: str, username: str, password: str, start_node: str, end_node: str, **kwargs):
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

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.find_shortest_path(
            self.db_url,
            self.username,
            self.password,
            arguments.get("start_node"),
            arguments.get("end_node"),
            relationshipWeightProperty=arguments.get("relationship_property")
        )