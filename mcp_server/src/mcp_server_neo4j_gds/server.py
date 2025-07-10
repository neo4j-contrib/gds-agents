# server.py
import logging
from fastmcp import FastMCP
import pandas as pd
import json
from typing import Any, Dict
from graphdatascience import GraphDataScience
from .registry import AlgorithmRegistry
from .gds import count_nodes, get_node_properties_keys
from .centrality_algorithm_specs import centrality_tool_definitions
from .community_algorithm_specs import community_tool_definitions
from .path_algorithm_specs import path_tool_definitions
from .similarity_algorithm_specs import similarity_tool_definitions

logger = logging.getLogger("mcp_server_neo4j_gds")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("mcp_server_neo4j_gds.log"), logging.StreamHandler()],
)


def serialize_result(result: Any) -> str:
    """Serialize results to string without truncation, handling DataFrames specially"""
    if isinstance(result, pd.DataFrame):
        # Configure pandas to show all rows and columns
        with pd.option_context(
            "display.max_rows",
            None,
            "display.max_columns",
            None,
            "display.width",
            None,
            "display.max_colwidth",
            None,
        ):
            return result.to_string(index=True)
    elif isinstance(result, (list, dict)):
        # Use JSON for better formatting of complex data structures
        return json.dumps(result, indent=2, default=str)
    else:
        # For other types, use string conversion
        return str(result)


def create_algorithm_tool(mcp: FastMCP, tool_name: str, gds: GraphDataScience):
    """Create and register an algorithm tool with proper closure"""

    async def algorithm_tool(parameters: Dict[str, Any] = None) -> str:
        """Execute algorithm tool with parameters dictionary"""
        try:
            handler = AlgorithmRegistry.get_handler(tool_name, gds)
            result = handler.execute(parameters or {})
            return serialize_result(result)
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

    # Set the function name and docstring
    algorithm_tool.__name__ = tool_name
    algorithm_tool.__doc__ = f"Execute {tool_name} algorithm with parameters dictionary"

    # Register the tool with the server
    mcp.tool(algorithm_tool)


def main(db_url: str, username: str, password: str, database: str = None):
    """Main function that sets up and runs the FastMCP server"""
    logger.info(f"Starting MCP Server for {db_url} with username {username}")
    if database:
        logger.info(f"Connecting to database: {database}")

    # Create GraphDataScience object with optional database parameter
    if database:
        gds = GraphDataScience(
            db_url, auth=(username, password), aura_ds=False, database=database
        )
    else:
        gds = GraphDataScience(db_url, auth=(username, password), aura_ds=False)

    # Create FastMCP server
    mcp = FastMCP("neo4j-gds")

    # Register basic tools using the correct decorator - renamed to avoid conflicts
    @mcp.tool
    async def count_nodes_tool() -> str:
        """Count the number of nodes in the graph"""
        result = count_nodes(gds)
        return serialize_result(result)

    @mcp.tool
    async def get_node_properties_keys_tool() -> str:
        """Get all node properties keys in the database"""
        result = get_node_properties_keys(gds)
        return serialize_result(result)

    # Add a list_tools tool that returns proper MCP Tool objects
    @mcp.tool
    async def list_tools() -> str:
        """List all available tools in MCP Tool format"""
        tools_list = []

        # Add basic tools
        tools_list.append(
            {
                "name": "count_nodes_tool",
                "description": "Count the number of nodes in the graph",
                "inputSchema": {"type": "object", "properties": {}, "required": []},
            }
        )

        tools_list.append(
            {
                "name": "get_node_properties_keys_tool",
                "description": "Get all node properties keys in the database",
                "inputSchema": {"type": "object", "properties": {}, "required": []},
            }
        )

        # Add algorithm tools from existing specs
        all_tool_definitions = (
            centrality_tool_definitions
            + community_tool_definitions
            + path_tool_definitions
            + similarity_tool_definitions
        )

        for tool_def in all_tool_definitions:
            tools_list.append(
                {
                    "name": tool_def.name,
                    "description": tool_def.description,
                    "inputSchema": tool_def.inputSchema,
                }
            )

        return json.dumps(tools_list, indent=2)

    # Get all algorithm names from the registry
    algorithm_names = list(AlgorithmRegistry._handlers.keys())

    # Create individual tool functions for each algorithm
    for tool_name in algorithm_names:
        create_algorithm_tool(mcp, tool_name, gds)

    # Run the server - FastMCP will handle the event loop
    mcp.run()


if __name__ == "__main__":
    import argparse
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv("../../../.env")

    parser = argparse.ArgumentParser(description="Neo4j GDS MCP Server")
    parser.add_argument(
        "--db-url", default=os.environ.get("NEO4J_URI"), help="URL to Neo4j database"
    )
    parser.add_argument(
        "--username",
        default=os.environ.get("NEO4J_USERNAME", "neo4j"),
        help="Username for Neo4j database",
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("NEO4J_PASSWORD"),
        help="Password for Neo4j database",
    )
    parser.add_argument(
        "--database",
        default=os.environ.get("NEO4J_DATABASE"),
        help="Database name to connect to (optional). By default, the server will connect to the 'neo4j' database.",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("mcp_server_neo4j_gds.log"),
            logging.StreamHandler(),
        ],
    )

    logging.info(f"Starting MCP Server for {args.db_url} with username {args.username}")
    if args.database:
        logging.info(f"Connecting to database: {args.database}")

    main(
        db_url=args.db_url,
        username=args.username,
        password=args.password,
        database=args.database,
    )
