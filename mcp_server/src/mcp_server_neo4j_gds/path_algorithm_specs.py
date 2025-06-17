from mcp import types

path_tool_definitions = [
    types.Tool(
        name="find_shortest_path",
        description="Find the shortest path between two nodes using Dijkstra's algorithm",
        inputSchema={
            "type": "object",
            "properties": {
                "start_node": {"type": "string", "description": "Name of the starting node"},
                "end_node": {"type": "string", "description": "Name of the ending node"},
                "relationship_property": {
                    "type": "string",
                    "description": "Property of the relationship to use for path finding"
                }
            },
            "required": ["start_node", "end_node"]
        }
    ),
    types.Tool(
        name="delta_stepping_shortest_path",
        description="The Delta-Stepping Shortest Path algorithm computes all shortest paths between a source node and all reachable nodes in the graph. "
                   "The algorithm supports weighted graphs with positive relationship weights. To compute the shortest path between a source and a single target node, Dijkstra Source-Target can be used. "
                   "In contrast to Dijkstra Single-Source, the Delta-Stepping algorithm is a distance correcting algorithm. "
                   "This property allows it to traverse the graph in parallel. The algorithm is guaranteed to always find the shortest path between a source node and a target node. "
                   "However, if multiple shortest paths exist between two nodes, the algorithm is not guaranteed to return the same path in each computation.",
        inputSchema={
            "type": "object",
            "properties": {
                "sourceNode": {
                    "type": "string",
                    "description": "Name of the source node to find shortest paths from."
                },
                "delta": {
                    "type": "number",
                    "description": "The bucket width for grouping nodes with the same tentative distance to the source node."
                },
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "Name of the relationship property to use as weights. If unspecified, the algorithm runs unweighted."
                }
            },
            "required": ["sourceNode"]
        }
    ),
    types.Tool(
        name="dijkstra_single_source_shortest_path",
        description="The Dijkstra Shortest Path algorithm computes the shortest path between nodes. "
                   "The algorithm supports weighted graphs with positive relationship weights. "
                   "The Dijkstra Single-Source algorithm computes the shortest paths between a source node and all nodes reachable from that node. "
                   "To compute the shortest path between a source and a target node, Dijkstra Source-Target can be used.",
        inputSchema={
            "type": "object",
            "properties": {
                "sourceNode": {
                    "type": "string",
                    "description": "Name of the source node to find shortest paths from."
                },
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "Name of the relationship property to use as weights. If unspecified, the algorithm runs unweighted."
                }
            },
            "required": ["sourceNode"]
        }
    ),
    types.Tool(
        name="a_star_shortest_path",
        description="The A* (pronounced \"A-Star\") Shortest Path algorithm computes the shortest path between two nodes. "
                   "A* is an informed search algorithm as it uses a heuristic function to guide the graph traversal. "
                   "The algorithm supports weighted graphs with positive relationship weights. "
                   "Unlike Dijkstra's shortest path algorithm, the next node to search from is not solely picked on the already computed distance. "
                   "Instead, the algorithm combines the already computed distance with the result of a heuristic function. "
                   "That function takes a node as input and returns a value that corresponds to the cost to reach the target node from that node. "
                   "In each iteration, the graph traversal is continued from the node with the lowest combined cost. "
                   "In GDS, the A* algorithm is based on the Dijkstra's shortest path algorithm. "
                   "The heuristic function is the haversine distance, which defines the distance between two points on a sphere. "
                   "Here, the sphere is the earth and the points are geo-coordinates stored on the nodes in the graph.",
        inputSchema={
            "type": "object",
            "properties": {
                "sourceNode": {
                    "type": "string",
                    "description": "Name of the source node to find shortest path from."
                },
                "targetNode": {
                    "type": "string",
                    "description": "Name of the target node to find shortest path to."
                },
                "latitudeProperty": {
                    "type": "string",
                    "description": "The node property that stores the latitude value."
                },
                "longitudeProperty": {
                    "type": "string",
                    "description": "The node property that stores the longitude value."
                },
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "Name of the relationship property to use as weights. If unspecified, the algorithm runs unweighted."
                }
            },
            "required": ["sourceNode", "targetNode"]
        }
    ),
    types.Tool(
        name="yens_shortest_paths",
        description="Yen's Shortest Path algorithm computes a number of shortest paths between two nodes. "
                   "The algorithm is often referred to as Yen's k-Shortest Path algorithm, where k is the number of shortest paths to compute. "
                   "The algorithm supports weighted graphs with positive relationship weights. "
                   "It also respects parallel relationships between the same two nodes when computing multiple shortest paths. "
                   "For k = 1, the algorithm behaves exactly like Dijkstra's shortest path algorithm and returns the shortest path. "
                   "For k = 2, the algorithm returns the shortest path and the second shortest path between the same source and target node. "
                   "Generally, for k = n, the algorithm computes at most n paths which are discovered in the order of their total cost. "
                   "The GDS implementation is based on the original description. "
                   "For the actual path computation, Yen's algorithm uses Dijkstra's shortest path algorithm. "
                   "The algorithm makes sure that an already discovered shortest path will not be traversed again.",
        inputSchema={
            "type": "object",
            "properties": {
                "sourceNode": {
                    "type": "string",
                    "description": "Name of the source node to find shortest paths from."
                },
                "targetNode": {
                    "type": "string",
                    "description": "Name of the target node to find shortest paths to."
                },
                "k": {
                    "type": "integer",
                    "description": "The number of shortest paths to compute between source and target node."
                },
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "Name of the relationship property to use as weights. If unspecified, the algorithm runs unweighted."
                }
            },
            "required": ["sourceNode", "targetNode"]
        }
    )
]