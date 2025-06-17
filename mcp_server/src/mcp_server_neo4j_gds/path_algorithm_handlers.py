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


class DeltaSteppingShortestPathHandler(AlgorithmHandler):
    def delta_stepping_shortest_path(self, db_url: str, username: str, password: str, source_node: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)

        query = """
        MATCH (source)
        WHERE toLower(source.name) CONTAINS toLower($source_name)
        RETURN id(source) as source_id
        """

        df = gds.run_cypher(
            query,
            params={
                'source_name': source_node
            }
        )

        if df.empty:
            return {
                "found": False,
                "message": "Source node name not found"
            }

        source_node_id = int(df['source_id'].iloc[0])

        with projected_graph(gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Delta-Stepping shortest path parameters: {params}")

            path_data = gds.shortestPath.deltaStepping.stream(
                G,
                sourceNode=source_node_id,
                **params
            )

            if path_data.empty:
                return {
                    "found": False,
                    "message": "No paths found from the source node"
                }

            # Convert to native Python types as needed
            result_data = []
            for _, row in path_data.iterrows():
                node_id = int(row['targetNode'])
                cost = float(row['cost'])
                
                # Get node name using GDS utility function
                node_name = gds.util.asNode(node_id)
                
                result_data.append({
                    "targetNodeId": node_id,
                    "targetNodeName": node_name,
                    "cost": cost
                })

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": gds.util.asNode(source_node_id),
                "paths": result_data,
                "totalPaths": len(result_data)
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.delta_stepping_shortest_path(
            self.db_url,
            self.username,
            self.password,
            arguments.get("sourceNode"),
            delta=arguments.get("delta"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty")
        )


class DijkstraSingleSourceShortestPathHandler(AlgorithmHandler):
    def dijkstra_single_source_shortest_path(self, db_url: str, username: str, password: str, source_node: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)

        query = """
        MATCH (source)
        WHERE toLower(source.name) CONTAINS toLower($source_name)
        RETURN id(source) as source_id
        """

        df = gds.run_cypher(
            query,
            params={
                'source_name': source_node
            }
        )

        if df.empty:
            return {
                "found": False,
                "message": "Source node name not found"
            }

        source_node_id = int(df['source_id'].iloc[0])

        with projected_graph(gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Dijkstra single-source shortest path parameters: {params}")

            path_data = gds.shortestPath.dijkstra.stream(
                G,
                sourceNode=source_node_id,
                **params
            )

            if path_data.empty:
                return {
                    "found": False,
                    "message": "No paths found from the source node"
                }

            # Convert to native Python types as needed
            result_data = []
            for _, row in path_data.iterrows():
                node_id = int(row['targetNode'])
                cost = float(row['cost'])
                
                # Get node name using GDS utility function
                node_name = gds.util.asNode(node_id)
                
                result_data.append({
                    "targetNodeId": node_id,
                    "targetNodeName": node_name,
                    "cost": cost
                })

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": gds.util.asNode(source_node_id),
                "paths": result_data,
                "totalPaths": len(result_data)
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.dijkstra_single_source_shortest_path(
            self.db_url,
            self.username,
            self.password,
            arguments.get("sourceNode"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty")
        )


class AStarShortestPathHandler(AlgorithmHandler):
    def a_star_shortest_path(self, db_url: str, username: str, password: str, source_node: str, target_node: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)

        query = """
        MATCH (source)
        WHERE toLower(source.name) CONTAINS toLower($source_name)
        MATCH (target)
        WHERE toLower(target.name) CONTAINS toLower($target_name)
        RETURN id(source) as source_id, id(target) as target_id
        """

        df = gds.run_cypher(
            query,
            params={
                'source_name': source_node,
                'target_name': target_node
            }
        )

        if df.empty:
            return {
                "found": False,
                "message": "One or both node names not found"
            }

        source_node_id = int(df['source_id'].iloc[0])
        target_node_id = int(df['target_id'].iloc[0])

        with projected_graph(gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"A* shortest path parameters: {params}")

            path_data = gds.shortestPath.astar.stream(
                G,
                sourceNode=source_node_id,
                targetNode=target_node_id,
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
        return self.a_star_shortest_path(
            self.db_url,
            self.username,
            self.password,
            arguments.get("sourceNode"),
            arguments.get("targetNode"),
            latitudeProperty=arguments.get("latitudeProperty"),
            longitudeProperty=arguments.get("longitudeProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty")
        )


class YensShortestPathsHandler(AlgorithmHandler):
    def yens_shortest_paths(self, db_url: str, username: str, password: str, source_node: str, target_node: str, **kwargs):
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)

        query = """
        MATCH (source)
        WHERE toLower(source.name) CONTAINS toLower($source_name)
        MATCH (target)
        WHERE toLower(target.name) CONTAINS toLower($target_name)
        RETURN id(source) as source_id, id(target) as target_id
        """

        df = gds.run_cypher(
            query,
            params={
                'source_name': source_node,
                'target_name': target_node
            }
        )

        if df.empty:
            return {
                "found": False,
                "message": "One or both node names not found"
            }

        source_node_id = int(df['source_id'].iloc[0])
        target_node_id = int(df['target_id'].iloc[0])

        with projected_graph(gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Yen's shortest paths parameters: {params}")

            path_data = gds.shortestPath.yens.stream(
                G,
                sourceNode=source_node_id,
                targetNode=target_node_id,
                **params
            )

            if path_data.empty:
                return {
                    "found": False,
                    "message": "No paths found between the specified nodes"
                }

            # Convert to native Python types as needed
            result_data = []
            for _, row in path_data.iterrows():
                # Convert to native Python types as needed - handle both list and Series objects
                node_ids = row['nodeIds']
                costs = row['costs']

                # Convert only if not already a list
                if hasattr(node_ids, 'tolist'):
                    node_ids = node_ids.tolist()
                if hasattr(costs, 'tolist'):
                    costs = costs.tolist()

                # Get node names using GDS utility function
                node_names = [gds.util.asNode(node_id) for node_id in node_ids]

                result_data.append({
                    "index": int(row['index']),
                    "totalCost": float(row['totalCost']),
                    "nodeIds": node_ids,
                    "nodeNames": node_names,
                    "path": row['path'],
                    "costs": costs
                })

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": gds.util.asNode(source_node_id),
                "targetNodeId": target_node_id,
                "targetNodeName": gds.util.asNode(target_node_id),
                "paths": result_data,
                "totalPaths": len(result_data)
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.yens_shortest_paths(
            self.db_url,
            self.username,
            self.password,
            arguments.get("sourceNode"),
            arguments.get("targetNode"),
            k=arguments.get("k"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty")
        )