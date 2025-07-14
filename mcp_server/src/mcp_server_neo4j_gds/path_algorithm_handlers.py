import logging
from typing import Dict, Any


from .algorithm_handler import AlgorithmHandler
from .gds import projected_graph

logger = logging.getLogger("mcp_server_neo4j_gds")


class DijkstraShortestPathHandler(AlgorithmHandler):
    def find_shortest_path(
        self, start_node: str, end_node: str, node_identifier_property: str, **kwargs
    ):
        query = f"""
        MATCH (start)
        WHERE toLower(start.{node_identifier_property}) CONTAINS toLower($start_name)
        MATCH (end)
        WHERE toLower(end.{node_identifier_property}) CONTAINS toLower($end_name)
        RETURN id(start) as start_id, id(end) as end_id
        """

        df = self.gds.run_cypher(
            query, params={"start_name": start_node, "end_name": end_node}
        )

        if df.empty:
            return {"found": False, "message": "One or both node names not found"}

        start_node_id = int(df["start_id"].iloc[0])
        end_node_id = int(df["end_id"].iloc[0])

        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            args = locals()
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Dijkstra single-source shortest path parameters: {params}")

            path_data = self.gds.shortestPath.dijkstra.stream(
                G, sourceNode=start_node_id, targetNode=end_node_id, **params
            )

            if path_data.empty:
                return {
                    "found": False,
                    "message": "No path found between the specified nodes",
                }

            # Convert to native Python types as needed - handle both list and Series objects
            node_ids = path_data["nodeIds"].iloc[0]
            costs = path_data["costs"].iloc[0]

            # Convert only if not already a list
            if hasattr(node_ids, "tolist"):
                node_ids = node_ids.tolist()
            if hasattr(costs, "tolist"):
                costs = costs.tolist()

            # Get node names using GDS utility function
            node_names = [self.gds.util.asNode(node_id) for node_id in node_ids]

            return {
                "totalCost": float(path_data["totalCost"].iloc[0]),
                "nodeIds": node_ids,
                "nodeNames": node_names,
                "path": path_data["path"].iloc[0],
                "costs": costs,
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.find_shortest_path(
            arguments.get("start_node"),
            arguments.get("end_node"),
            arguments.get("nodeIdentifierProperty"),
            relationshipWeightProperty=arguments.get("relationship_property"),
        )


class DeltaSteppingShortestPathHandler(AlgorithmHandler):
    def delta_stepping_shortest_path(
        self, source_node: str, node_identifier_property: str, **kwargs
    ):
        query = f"""
        MATCH (source)
        WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
        RETURN id(source) as source_id
        """

        df = self.gds.run_cypher(query, params={"source_name": source_node})

        if df.empty:
            return {"found": False, "message": "Source node name not found"}

        source_node_id = int(df["source_id"].iloc[0])

        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Delta-Stepping shortest path parameters: {params}")

            path_data = self.gds.shortestPath.deltaStepping.stream(
                G, sourceNode=source_node_id, **params
            )

            if path_data.empty:
                return {
                    "found": False,
                    "message": "No paths found from the source node",
                }

            # Convert to native Python types as needed
            result_data = []
            for _, row in path_data.iterrows():
                node_id = int(row["targetNode"])
                cost = float(row["cost"])

                # Get node name using GDS utility function
                node_name = self.gds.util.asNode(node_id)

                result_data.append(
                    {"targetNodeId": node_id, "targetNodeName": node_name, "cost": cost}
                )

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": self.gds.util.asNode(source_node_id),
                "paths": result_data,
                "totalPaths": len(result_data),
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.delta_stepping_shortest_path(
            arguments.get("sourceNode"),
            arguments.get("nodeIdentifierProperty"),
            delta=arguments.get("delta"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class DijkstraSingleSourceShortestPathHandler(AlgorithmHandler):
    def dijkstra_single_source_shortest_path(
        self, source_node: str, node_identifier_property: str, **kwargs
    ):
        query = f"""
        MATCH (source)
        WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
        RETURN id(source) as source_id
        """

        df = self.gds.run_cypher(query, params={"source_name": source_node})

        if df.empty:
            return {"found": False, "message": "Source node name not found"}

        source_node_id = int(df["source_id"].iloc[0])

        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Dijkstra single-source shortest path parameters: {params}")

            path_data = self.gds.shortestPath.dijkstra.stream(
                G, sourceNode=source_node_id, **params
            )

            if path_data.empty:
                return {
                    "found": False,
                    "message": "No paths found from the source node",
                }

            # Convert to native Python types as needed
            result_data = []
            for _, row in path_data.iterrows():
                node_id = int(row["targetNode"])
                cost = float(row["cost"])

                # Get node name using GDS utility function
                node_name = self.gds.util.asNode(node_id)

                result_data.append(
                    {"targetNodeId": node_id, "targetNodeName": node_name, "cost": cost}
                )

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": self.gds.util.asNode(source_node_id),
                "paths": result_data,
                "totalPaths": len(result_data),
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.dijkstra_single_source_shortest_path(
            arguments.get("sourceNode"),
            arguments.get("nodeIdentifierProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class AStarShortestPathHandler(AlgorithmHandler):
    def a_star_shortest_path(
        self,
        source_node: str,
        target_node: str,
        node_identifier_property: str,
        **kwargs,
    ):
        query = f"""
        MATCH (source)
        WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
        MATCH (target)
        WHERE toLower(target.{node_identifier_property}) CONTAINS toLower($target_name)
        RETURN id(source) as source_id, id(target) as target_id
        """

        df = self.gds.run_cypher(
            query, params={"source_name": source_node, "target_name": target_node}
        )

        if df.empty:
            return {"found": False, "message": "One or both node names not found"}

        source_node_id = int(df["source_id"].iloc[0])
        target_node_id = int(df["target_id"].iloc[0])

        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"A* shortest path parameters: {params}")

            path_data = self.gds.shortestPath.astar.stream(
                G, sourceNode=source_node_id, targetNode=target_node_id, **params
            )

            if path_data.empty:
                return {
                    "found": False,
                    "message": "No path found between the specified nodes",
                }

            # Convert to native Python types as needed - handle both list and Series objects
            node_ids = path_data["nodeIds"].iloc[0]
            costs = path_data["costs"].iloc[0]

            # Convert only if not already a list
            if hasattr(node_ids, "tolist"):
                node_ids = node_ids.tolist()
            if hasattr(costs, "tolist"):
                costs = costs.tolist()

            # Get node names using GDS utility function
            node_names = [self.gds.util.asNode(node_id) for node_id in node_ids]

            return {
                "totalCost": float(path_data["totalCost"].iloc[0]),
                "nodeIds": node_ids,
                "nodeNames": node_names,
                "path": path_data["path"].iloc[0],
                "costs": costs,
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.a_star_shortest_path(
            arguments.get("sourceNode"),
            arguments.get("targetNode"),
            arguments.get("nodeIdentifierProperty"),
            latitudeProperty=arguments.get("latitudeProperty"),
            longitudeProperty=arguments.get("longitudeProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class YensShortestPathsHandler(AlgorithmHandler):
    def yens_shortest_paths(
        self,
        source_node: str,
        target_node: str,
        node_identifier_property: str,
        **kwargs,
    ):
        query = f"""
        MATCH (source)
        WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
        MATCH (target)
        WHERE toLower(target.{node_identifier_property}) CONTAINS toLower($target_name)
        RETURN id(source) as source_id, id(target) as target_id
        """

        df = self.gds.run_cypher(
            query, params={"source_name": source_node, "target_name": target_node}
        )

        if df.empty:
            return {"found": False, "message": "One or both node names not found"}

        source_node_id = int(df["source_id"].iloc[0])
        target_node_id = int(df["target_id"].iloc[0])

        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Yen's shortest paths parameters: {params}")

            path_data = self.gds.shortestPath.yens.stream(
                G, sourceNode=source_node_id, targetNode=target_node_id, **params
            )

            if path_data.empty:
                return {
                    "found": False,
                    "message": "No paths found between the specified nodes",
                }

            # Convert to native Python types as needed
            result_data = []
            for _, row in path_data.iterrows():
                # Convert to native Python types as needed - handle both list and Series objects
                node_ids = row["nodeIds"]
                costs = row["costs"]

                # Convert only if not already a list
                if hasattr(node_ids, "tolist"):
                    node_ids = node_ids.tolist()
                if hasattr(costs, "tolist"):
                    costs = costs.tolist()

                # Get node names using GDS utility function
                node_names = [self.gds.util.asNode(node_id) for node_id in node_ids]

                result_data.append(
                    {
                        "index": int(row["index"]),
                        "totalCost": float(row["totalCost"]),
                        "nodeIds": node_ids,
                        "nodeNames": node_names,
                        "path": row["path"],
                        "costs": costs,
                    }
                )

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": self.gds.util.asNode(source_node_id),
                "targetNodeId": target_node_id,
                "targetNodeName": self.gds.util.asNode(target_node_id),
                "paths": result_data,
                "totalPaths": len(result_data),
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.yens_shortest_paths(
            arguments.get("sourceNode"),
            arguments.get("targetNode"),
            arguments.get("nodeIdentifierProperty"),
            k=arguments.get("k"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class MinimumWeightSpanningTreeHandler(AlgorithmHandler):
    def minimum_weight_spanning_tree(
        self, source_node: str, node_identifier_property: str, **kwargs
    ):
        query = f"""
        MATCH (source)
        WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
        RETURN id(source) as source_id
        """

        df = self.gds.run_cypher(query, params={"source_name": source_node})

        if df.empty:
            return {"found": False, "message": "Source node name not found"}

        source_node_id = int(df["source_id"].iloc[0])

        with projected_graph(self.gds, undirected=True) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Minimum Weight Spanning Tree parameters: {params}")

            mst_data = self.gds.spanningTree.stream(
                G, sourceNode=source_node_id, **params
            )

            if mst_data.empty:
                return {
                    "found": False,
                    "message": "No spanning tree found from the source node",
                }

            # Convert to native Python types as needed
            result_data = []
            total_weight = 0.0

            for _, row in mst_data.iterrows():
                source_id = int(row["sourceNode"])
                target_id = int(row["targetNode"])
                weight = float(row["cost"])
                total_weight += weight

                # Get node names using GDS utility function
                source_name = self.gds.util.asNode(source_id)
                target_name = self.gds.util.asNode(target_id)

                result_data.append(
                    {
                        "sourceNodeId": source_id,
                        "sourceNodeName": source_name,
                        "targetNodeId": target_id,
                        "targetNodeName": target_name,
                        "cost": weight,
                    }
                )

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": self.gds.util.asNode(source_node_id),
                "totalWeight": total_weight,
                "relationships": result_data,
                "totalRelationships": len(result_data),
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.minimum_weight_spanning_tree(
            arguments.get("sourceNode"),
            arguments.get("nodeIdentifierProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            objective=arguments.get("objective"),
        )


class MinimumWeightKSpanningTreeHandler(AlgorithmHandler):
    def minimum_weight_k_spanning_tree(self, write_property: str, k: int, **kwargs):
        with projected_graph(self.gds, undirected=True) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Minimum Weight K-Spanning Tree parameters: {params}")

            # Run the k-spanning tree algorithm
            result = self.gds.kSpanningTree.write(
                G, writeProperty=write_property, k=k, **params
            )

            # The write procedure returns performance metrics and effectiveNodeCount
            # The results are written to the database with the specified writeProperty
            return {
                "found": True,
                "writeProperty": write_property,
                "k": k,
                "effectiveNodeCount": int(result["effectiveNodeCount"]),
                "preProcessingMillis": int(result["preProcessingMillis"]),
                "computeMillis": int(result["computeMillis"]),
                "writeMillis": int(result["writeMillis"]),
                "message": f"K-spanning tree with {result['effectiveNodeCount']} nodes written to property '{write_property}'",
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.minimum_weight_k_spanning_tree(
            arguments.get("writeProperty"),
            arguments.get("k"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            objective=arguments.get("objective"),
        )


class MinimumDirectedSteinerTreeHandler(AlgorithmHandler):
    def minimum_directed_steiner_tree(
        self,
        source_node: str,
        target_nodes: list,
        node_identifier_property: str,
        **kwargs,
    ):
        # Find source node ID
        source_query = f"""
        MATCH (source)
        WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
        RETURN id(source) as source_id
        """

        source_df = self.gds.run_cypher(
            source_query, params={"source_name": source_node}
        )

        if source_df.empty:
            return {"found": False, "message": "Source node name not found"}

        source_node_id = int(source_df["source_id"].iloc[0])

        # Find target node IDs - ensure ALL target nodes are found
        target_node_ids = []
        target_node_names = []
        unmatched_targets = []

        for target_name in target_nodes:
            target_query = f"""
            MATCH (target)
            WHERE toLower(target.{node_identifier_property}) CONTAINS toLower($target_name)
            RETURN id(target) as target_id, target.{node_identifier_property} as target_name
            """

            target_df = self.gds.run_cypher(
                target_query, params={"target_name": target_name}
            )

            if not target_df.empty:
                target_node_ids.append(int(target_df["target_id"].iloc[0]))
                target_node_names.append(target_df["target_name"].iloc[0])
            else:
                unmatched_targets.append(target_name)

        # Check if all target nodes were found
        if unmatched_targets:
            return {
                "found": False,
                "message": f"The following target nodes were not found: {', '.join(unmatched_targets)}",
            }

        if not target_node_ids:
            return {"found": False, "message": "No target nodes found"}

        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Minimum Directed Steiner Tree parameters: {params}")

            # Run the steiner tree algorithm
            steiner_data = self.gds.steinerTree.stream(
                G, sourceNode=source_node_id, targetNodes=target_node_ids, **params
            )

            if steiner_data.empty:
                return {
                    "found": False,
                    "message": "No steiner tree found connecting the source to all target nodes",
                }

            # Convert to native Python types as needed
            result_data = []
            total_weight = 0.0

            for _, row in steiner_data.iterrows():
                source_id = int(row["sourceNode"])
                target_id = int(row["targetNode"])
                weight = float(row["cost"])
                total_weight += weight

                # Get node names using GDS utility function
                source_name = self.gds.util.asNode(source_id)
                target_name = self.gds.util.asNode(target_id)

                result_data.append(
                    {
                        "sourceNodeId": source_id,
                        "sourceNodeName": source_name,
                        "targetNodeId": target_id,
                        "targetNodeName": target_name,
                        "cost": weight,
                    }
                )

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": self.gds.util.asNode(source_node_id),
                "targetNodes": target_node_names,
                "targetNodeIds": target_node_ids,
                "totalWeight": total_weight,
                "relationships": result_data,
                "totalRelationships": len(result_data),
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.minimum_directed_steiner_tree(
            arguments.get("sourceNode"),
            arguments.get("targetNodes"),
            arguments.get("nodeIdentifierProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            delta=arguments.get("delta"),
            applyRerouting=arguments.get("applyRerouting"),
        )


class PrizeCollectingSteinerTreeHandler(AlgorithmHandler):
    def prize_collecting_steiner_tree(self, **kwargs):
        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Prize-Collecting Steiner Tree parameters: {params}")

            # Run the prize-collecting steiner tree algorithm
            steiner_data = self.gds.prizeSteinerTree.stream(G, **params)

            if steiner_data.empty:
                return {
                    "found": False,
                    "message": "No prize-collecting steiner tree found",
                }

            # Convert to native Python types as needed
            result_data = []
            total_weight = 0.0
            total_prize = 0.0

            for _, row in steiner_data.iterrows():
                source_id = int(row["sourceNode"])
                target_id = int(row["targetNode"])
                weight = float(row["cost"])
                total_weight += weight

                # Get node names using GDS utility function
                source_name = self.gds.util.asNode(source_id)
                target_name = self.gds.util.asNode(target_id)

                result_data.append(
                    {
                        "sourceNodeId": source_id,
                        "sourceNodeName": source_name,
                        "targetNodeId": target_id,
                        "targetNodeName": target_name,
                        "cost": weight,
                    }
                )

            # Calculate total prize from nodes in the tree
            if "prizeProperty" in params:
                prize_query = f"""
                MATCH (n)
                WHERE n.{params["prizeProperty"]} IS NOT NULL
                RETURN sum(n.{params["prizeProperty"]}) as totalPrize
                """
                prize_df = self.gds.run_cypher(prize_query)
                if not prize_df.empty:
                    total_prize = float(prize_df["totalPrize"].iloc[0])

            return {
                "found": True,
                "totalWeight": total_weight,
                "totalPrize": total_prize,
                "netValue": total_prize - total_weight,
                "relationships": result_data,
                "totalRelationships": len(result_data),
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.prize_collecting_steiner_tree(
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            prizeProperty=arguments.get("prizeProperty"),
        )


class AllPairsShortestPathsHandler(AlgorithmHandler):
    def all_pairs_shortest_paths(self, **kwargs):
        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"All Pairs Shortest Paths parameters: {params}")

            # Run the all pairs shortest paths algorithm
            apsp_data = self.gds.allShortestPaths.stream(G, **params)

            if apsp_data.empty:
                return {"found": False, "message": "No shortest paths found"}

            # Convert to native Python types as needed
            result_data = []
            finite_paths = 0
            infinite_paths = 0

            for _, row in apsp_data.iterrows():
                source_id = int(row["sourceNode"])
                target_id = int(row["targetNode"])
                cost = row["cost"]

                # Check if the cost is finite (not infinity)
                is_finite = self.gds.util.isFinite(cost)

                if is_finite:
                    finite_paths += 1
                    cost_value = float(cost)
                else:
                    infinite_paths += 1
                    cost_value = float("inf")

                # Get node names using GDS utility function
                source_name = self.gds.util.asNode(source_id)
                target_name = self.gds.util.asNode(target_id)

                result_data.append(
                    {
                        "sourceNodeId": source_id,
                        "sourceNodeName": source_name,
                        "targetNodeId": target_id,
                        "targetNodeName": target_name,
                        "cost": cost_value,
                        "isFinite": is_finite,
                    }
                )

            return {
                "found": True,
                "totalPairs": len(result_data),
                "finitePaths": finite_paths,
                "infinitePaths": infinite_paths,
                "paths": result_data,
                "message": f"Found {finite_paths} finite paths and {infinite_paths} infinite paths between all pairs of nodes",
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.all_pairs_shortest_paths(
            relationshipWeightProperty=arguments.get("relationshipWeightProperty")
        )


class RandomWalkHandler(AlgorithmHandler):
    def random_walk(self, **kwargs):
        # Process source nodes if provided
        source_node_ids = []
        if "sourceNodes" in kwargs and kwargs["sourceNodes"]:
            node_identifier_property = kwargs.get("nodeIdentifierProperty")
            if not node_identifier_property:
                return {
                    "found": False,
                    "message": "nodeIdentifierProperty is required when sourceNodes are provided",
                }

            for source_name in kwargs["sourceNodes"]:
                source_query = f"""
                MATCH (source)
                WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
                RETURN id(source) as source_id
                """

                source_df = self.gds.run_cypher(
                    source_query, params={"source_name": source_name}
                )

                if not source_df.empty:
                    source_node_ids.append(int(source_df["source_id"].iloc[0]))

        with projected_graph(self.gds) as G:
            # Prepare parameters for the random walk algorithm
            params = {k: v for k, v in kwargs.items() if v is not None}

            # Add source nodes if found
            if source_node_ids:
                params["sourceNodes"] = source_node_ids

            logger.info(f"Random Walk parameters: {params}")

            # Run the random walk algorithm
            walk_data = self.gds.randomWalk.stream(G, **params)

            if walk_data.empty:
                return {"found": False, "message": "No random walks generated"}

            # Convert to native Python types as needed
            result_data = []
            total_walks = 0

            for _, row in walk_data.iterrows():
                walk_id = int(row["walkId"])
                path = row["path"]

                # Convert path to list of node names
                node_names = []
                for node_id in path:
                    node_name = self.gds.util.asNode(node_id)
                    node_names.append(node_name)

                result_data.append(
                    {"walkId": walk_id, "path": node_names, "pathLength": len(path)}
                )
                total_walks += 1

            return {
                "found": True,
                "totalWalks": total_walks,
                "walks": result_data,
                "message": f"Generated {total_walks} random walks",
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.random_walk(
            sourceNodes=arguments.get("sourceNodes"),
            nodeIdentifierProperty=arguments.get("nodeIdentifierProperty"),
            walkLength=arguments.get("walkLength"),
            walksPerNode=arguments.get("walksPerNode"),
            inOutFactor=arguments.get("inOutFactor"),
            returnFactor=arguments.get("returnFactor"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
            walkBufferSize=arguments.get("walkBufferSize"),
        )


class BreadthFirstSearchHandler(AlgorithmHandler):
    def breadth_first_search(
        self, source_node: str, node_identifier_property: str, **kwargs
    ):
        # Find source node ID
        source_query = f"""
        MATCH (source)
        WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
        RETURN id(source) as source_id
        """

        source_df = self.gds.run_cypher(
            source_query, params={"source_name": source_node}
        )

        if source_df.empty:
            return {"found": False, "message": "Source node name not found"}

        source_node_id = int(source_df["source_id"].iloc[0])

        # Process target nodes if provided
        target_node_ids = []
        if "targetNodes" in kwargs and kwargs["targetNodes"]:
            for target_name in kwargs["targetNodes"]:
                target_query = f"""
                MATCH (target)
                WHERE toLower(target.{node_identifier_property}) CONTAINS toLower($target_name)
                RETURN id(target) as target_id
                """

                target_df = self.gds.run_cypher(
                    target_query, params={"target_name": target_name}
                )

                if not target_df.empty:
                    target_node_ids.append(int(target_df["target_id"].iloc[0]))

        with projected_graph(self.gds) as G:
            # Prepare parameters for the BFS algorithm
            params = {k: v for k, v in kwargs.items() if v is not None}

            # Add target nodes if found
            if target_node_ids:
                params["targetNodes"] = target_node_ids

            logger.info(f"Breadth First Search parameters: {params}")

            # Run the breadth first search algorithm
            bfs_data = self.gds.bfs.stream(G, sourceNode=source_node_id, **params)

            if bfs_data.empty:
                return {
                    "found": False,
                    "message": "No nodes visited in breadth first search",
                }

            # Convert to native Python types as needed
            result_data = []
            visited_nodes = 0

            for _, row in bfs_data.iterrows():
                node_id = int(row["nodeId"])
                depth = int(row["depth"])

                # Get node name using GDS utility function
                node_name = self.gds.util.asNode(node_id)

                result_data.append(
                    {"nodeId": node_id, "nodeName": node_name, "depth": depth}
                )
                visited_nodes += 1

            # Sort by depth for better readability
            result_data.sort(key=lambda x: x["depth"])

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": self.gds.util.asNode(source_node_id),
                "visitedNodes": visited_nodes,
                "nodes": result_data,
                "maxDepthReached": max([node["depth"] for node in result_data])
                if result_data
                else 0,
                "message": f"Visited {visited_nodes} nodes starting from '{self.gds.util.asNode(source_node_id)}'",
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.breadth_first_search(
            arguments.get("sourceNode"),
            arguments.get("nodeIdentifierProperty"),
            targetNodes=arguments.get("targetNodes"),
            maxDepth=arguments.get("maxDepth"),
        )


class DepthFirstSearchHandler(AlgorithmHandler):
    def depth_first_search(
        self, source_node: str, node_identifier_property: str, **kwargs
    ):
        # Find source node ID
        source_query = f"""
        MATCH (source)
        WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
        RETURN id(source) as source_id
        """

        source_df = self.gds.run_cypher(
            source_query, params={"source_name": source_node}
        )

        if source_df.empty:
            return {"found": False, "message": "Source node name not found"}

        source_node_id = int(source_df["source_id"].iloc[0])

        # Process target nodes if provided
        target_node_ids = []
        if "targetNodes" in kwargs and kwargs["targetNodes"]:
            for target_name in kwargs["targetNodes"]:
                target_query = f"""
                MATCH (target)
                WHERE toLower(target.{node_identifier_property}) CONTAINS toLower($target_name)
                RETURN id(target) as target_id
                """

                target_df = self.gds.run_cypher(
                    target_query, params={"target_name": target_name}
                )

                if not target_df.empty:
                    target_node_ids.append(int(target_df["target_id"].iloc[0]))

        with projected_graph(self.gds) as G:
            # Prepare parameters for the DFS algorithm
            params = {k: v for k, v in kwargs.items() if v is not None}

            # Add target nodes if found
            if target_node_ids:
                params["targetNodes"] = target_node_ids

            logger.info(f"Depth First Search parameters: {params}")

            # Run the depth first search algorithm
            dfs_data = self.gds.dfs.stream(G, sourceNode=source_node_id, **params)

            if dfs_data.empty:
                return {
                    "found": False,
                    "message": "No nodes visited in depth first search",
                }

            # Convert to native Python types as needed
            result_data = []
            visited_nodes = 0

            for _, row in dfs_data.iterrows():
                node_id = int(row["nodeId"])
                depth = int(row["depth"])

                # Get node name using GDS utility function
                node_name = self.gds.util.asNode(node_id)

                result_data.append(
                    {"nodeId": node_id, "nodeName": node_name, "depth": depth}
                )
                visited_nodes += 1

            # Sort by depth for better readability
            result_data.sort(key=lambda x: x["depth"])

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": self.gds.util.asNode(source_node_id),
                "visitedNodes": visited_nodes,
                "nodes": result_data,
                "maxDepthReached": max([node["depth"] for node in result_data])
                if result_data
                else 0,
                "message": f"Visited {visited_nodes} nodes starting from '{self.gds.util.asNode(source_node_id)}'",
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.depth_first_search(
            arguments.get("sourceNode"),
            arguments.get("nodeIdentifierProperty"),
            targetNodes=arguments.get("targetNodes"),
            maxDepth=arguments.get("maxDepth"),
        )


class BellmanFordSingleSourceShortestPathHandler(AlgorithmHandler):
    def bellman_ford_single_source_shortest_path(
        self, source_node: str, node_identifier_property: str, **kwargs
    ):
        # Find source node ID
        source_query = f"""
        MATCH (source)
        WHERE toLower(source.{node_identifier_property}) CONTAINS toLower($source_name)
        RETURN id(source) as source_id
        """

        source_df = self.gds.run_cypher(
            source_query, params={"source_name": source_node}
        )

        if source_df.empty:
            return {"found": False, "message": "Source node name not found"}

        source_node_id = int(source_df["source_id"].iloc[0])

        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(
                f"Bellman-Ford Single-Source Shortest Path parameters: {params}"
            )

            # Run the Bellman-Ford algorithm
            bellman_ford_data = self.gds.bellmanFord.stream(
                G, sourceNode=source_node_id, **params
            )

            if bellman_ford_data.empty:
                return {
                    "found": False,
                    "message": "No paths found from the source node",
                }

            # Convert to native Python types as needed
            result_data = []
            negative_cycles = []

            for _, row in bellman_ford_data.iterrows():
                node_id = int(row["targetNode"])
                cost = row["cost"]

                # Check if the cost is finite (not infinity)
                is_finite = self.gds.util.isFinite(cost)

                if is_finite:
                    cost_value = float(cost)
                else:
                    cost_value = float("inf")

                # Get node name using GDS utility function
                node_name = self.gds.util.asNode(node_id)

                result_data.append(
                    {
                        "targetNodeId": node_id,
                        "targetNodeName": node_name,
                        "cost": cost_value,
                        "isFinite": is_finite,
                    }
                )

            # Check for negative cycles in the result
            # If there are negative cycles, the algorithm might return them instead of shortest paths
            if "negativeCycle" in bellman_ford_data.columns:
                for _, row in bellman_ford_data.iterrows():
                    if "negativeCycle" in row and row["negativeCycle"] is not None:
                        cycle = row["negativeCycle"]
                        if hasattr(cycle, "tolist"):
                            cycle = cycle.tolist()

                        # Convert cycle node IDs to names
                        cycle_names = [
                            self.gds.util.asNode(node_id) for node_id in cycle
                        ]
                        negative_cycles.append(
                            {"cycle": cycle_names, "cycleLength": len(cycle)}
                        )

            return {
                "found": True,
                "sourceNodeId": source_node_id,
                "sourceNodeName": self.gds.util.asNode(source_node_id),
                "paths": result_data,
                "totalPaths": len(result_data),
                "negativeCycles": negative_cycles,
                "hasNegativeCycles": len(negative_cycles) > 0,
                "message": f"Found {len(result_data)} paths from '{self.gds.util.asNode(source_node_id)}'"
                + (
                    f" and {len(negative_cycles)} negative cycles"
                    if negative_cycles
                    else ""
                ),
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.bellman_ford_single_source_shortest_path(
            arguments.get("sourceNode"),
            arguments.get("nodeIdentifierProperty"),
            relationshipWeightProperty=arguments.get("relationshipWeightProperty"),
        )


class LongestPathHandler(AlgorithmHandler):
    def longest_path(self, **kwargs):
        with projected_graph(self.gds) as G:
            # If any optional parameter is not None, use that parameter
            params = {k: v for k, v in kwargs.items() if v is not None}
            logger.info(f"Longest Path parameters: {params}")

            # Run the longest path algorithm
            longest_path_data = self.gds.dag.longestPath.stream(G, **params)

            if longest_path_data.empty:
                return {
                    "found": False,
                    "message": "No longest paths found. The graph may contain cycles or be empty.",
                }

            # Convert to native Python types as needed
            result_data = []
            total_weight = 0.0

            for _, row in longest_path_data.iterrows():
                node_id = int(row["nodeId"])
                cost = row["cost"]

                # Check if the cost is finite (not infinity)
                is_finite = self.gds.util.isFinite(cost)

                if is_finite:
                    cost_value = float(cost)
                    total_weight += cost_value
                else:
                    cost_value = float("inf")

                # Get node name using GDS utility function
                node_name = self.gds.util.asNode(node_id)

                result_data.append(
                    {
                        "nodeId": node_id,
                        "nodeName": node_name,
                        "longestPathCost": cost_value,
                        "isFinite": is_finite,
                    }
                )

            # Sort by cost for better readability (highest first)
            result_data.sort(
                key=lambda x: x["longestPathCost"] if x["isFinite"] else float("inf"),
                reverse=True,
            )

            return {
                "found": True,
                "nodes": result_data,
                "totalNodes": len(result_data),
                "totalWeight": total_weight,
                "maxLongestPath": max(
                    [
                        node["longestPathCost"]
                        for node in result_data
                        if node["isFinite"]
                    ]
                )
                if any(node["isFinite"] for node in result_data)
                else 0,
                "message": f"Found longest paths for {len(result_data)} nodes in DAG components",
            }

    def execute(self, arguments: Dict[str, Any]) -> Any:
        return self.longest_path(
            relationshipWeightProperty=arguments.get("relationshipWeightProperty")
        )
