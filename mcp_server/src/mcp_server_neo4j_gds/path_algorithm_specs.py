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
]