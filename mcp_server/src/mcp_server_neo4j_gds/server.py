# server.py
import logging
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.types as types
from typing import Any
import mcp.server.stdio
from . import gds

logger = logging.getLogger('mcp_server_neo4j_gds')



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
                    "properties": {},
                    "required": [],
                },
            ),
            types.Tool(
                name="run_node_similarity",
                description="Run node similarity algorithm on the graph",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "node_label": {"type": "string", "description": "Label of nodes to analyze"},
                        "relationship_type": {"type": "string", "description": "Type of relationships to consider"},
                        "top_k": {"type": "integer", "description": "Number of similar pairs to return per node", "default": 10}
                    },
                    "required": ["node_label", "relationship_type"]
                },
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
                result = gds.count_nodes(db_url, username, password)
                return [types.TextContent(type="text", text=str(result))]

            elif name == "run_node_similarity":
                result = gds.run_node_similarity(
                    db_url,
                    username,
                    password,
                    arguments["node_label"],
                    arguments["relationship_type"],
                    arguments.get("top_k", 10)
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