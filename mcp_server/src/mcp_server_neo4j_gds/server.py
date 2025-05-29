# server.py
import logging
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.types as types
from typing import Any
import mcp.server.stdio
from . import gds
from .centrality_algorithm_specs import centrality_tool_definitions
from .path_algorithm_specs import path_tool_definitions
from .registry import AlgorithmRegistry

logger = logging.getLogger('mcp_server_neo4j_gds')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_server_neo4j_gds.log"),
        logging.StreamHandler()
    ]
)

async def main(db_url: str, username: str, password: str):
    logger.info(f"Starting MCP Server for {db_url} with username {username}")
    server = Server("example-server")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="count_nodes",
                description="""Count the number of nodes in the graph""",
                inputSchema={
                    "type": "object",
                },
            ),
            types.Tool(
                name="get_node_properties_keys",
                description="""Get all node properties keys in the database""",
                inputSchema={
                    "type": "object",
                },
            ),
        ] + centrality_tool_definitions + path_tool_definitions
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if name == "count_nodes":
                result = gds.count_nodes(db_url, username, password)
                return [types.TextContent(type="text", text=str(result))]

            elif name == "get_node_properties_keys":
                result = gds.get_node_properties_keys(db_url, username, password)
                return [types.TextContent(type="text", text=str(result))]

            else:
                handler = AlgorithmRegistry.get_handler(name, db_url, username, password)
                result = handler.execute(arguments or {})
                return [types.TextContent(type="text", text=str(result))]

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
                raise_exceptions=True,
            )