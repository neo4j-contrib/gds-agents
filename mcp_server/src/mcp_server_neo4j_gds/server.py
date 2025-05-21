# server.py
import logging
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.types as types
from typing import Any
import mcp.server.stdio
from . import gds

logger = logging.getLogger('mcp_server_neo4j_gds')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_server_neo4j_gds.log"),
        logging.StreamHandler()
    ]
)

def add(a: int, b: int) -> int:
    return a + b


async def main(db_url: str, username: str, password: str):
    logger.info(f"Starting MCP Server for {db_url} with username {username}")
    server = Server("example-server")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="add",
                description="""Add two numbers""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer", "description": "First number to add"},
                        "b": {"type": "integer", "description": "Second number to add"}
                    },
                    "required": ["a", "b"],
                },
            ),
            types.Tool(
                name="count_nodes",
                description="""Count the number of nodes in the graph""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "relationship_property": {"type": "string", "description": "Property of the relationship to use", "default": "distance"}
                    },
                    "required": ["relationship_property"]
                },
            ),
            types.Tool(
                name="degree_centrality",
                description="""Calculate degree centrality for all nodes in the graph""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "stations": {"type": "array", "items": {"type": "string"}, "description": "List of stations to return the centrality for"},
                    },
                    "required": [],
                },
            ),
            types.Tool(
                name="pagerank",
                description="""Calculate PageRank for all nodes in the graph""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "stations": {"type": "array", "items": {"type": "string"}, "description": "List of stations to return the PageRank for."},
                        "dampingFactor": {"type": "number", "description": "The damping factor of the Page Rank calculation. Must be in [0, 1)."},
                        "maxIterations": {"type": "integer", "description": "Maximum number of iterations for PageRank"},
                        "tolerance": {"type": "number", "description": "Minimum change in scores between iterations. If all scores change less than the tolerance value the result is considered stable and the algorithm returns."}
                    },
                    "required": [],
                },
            ),
            types.Tool(
                name="find_shortest_path",
                description="Find the shortest path between two stations using Dijkstra's algorithm",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "start_station": {"type": "string", "description": "Name of the starting station"},
                        "end_station": {"type": "string", "description": "Name of the ending station"},
                        "relationship_property": {
                            "type": "string", 
                            "description": "Property of the relationship to use for path finding",
                            "enum": ["distance", "time"],
                            "default": "distance"
                        }
                    },
                    "required": ["start_station", "end_station", "relationship_property"]
                }
            ),
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if name == "add":
                result = add(arguments["a"], arguments["b"])
                return [types.TextContent(type="text", text=str(result))]

            elif name == "count_nodes":
                result = gds.count_nodes(db_url, username, password, arguments["relationship_property"])
                return [types.TextContent(type="text", text=str(result))]

            elif name == "degree_centrality":
                result = gds.degree_centrality(db_url, username, password, arguments.get("stations"))
                return [types.TextContent(type="text", text=str(result))]

            elif name == "pagerank":
                # I want to optionally get the arguments["stations"] and pass them to the gds.pagerank function
                # if they are not None
                # and also pass the other arguments
                result = gds.pagerank(
                    db_url,
                    username,
                    password,
                    stations=arguments.get("stations"),
                    dampingFactor=arguments.get("dampingFactor"),
                    maxIterations=arguments.get("maxIterations"),
                    tolerance=arguments.get("tolerance")
                )
                return [types.TextContent(type="text", text=str(result))]
            
            elif name == "find_shortest_path":
                result = gds.find_shortest_path(
                    db_url,
                    username,
                    password,
                    arguments["start_station"],
                    arguments["end_station"],
                    arguments["relationship_property"]
                )
                return [types.TextContent(type="text", text=str(result))]
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="neo4j_gds",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )