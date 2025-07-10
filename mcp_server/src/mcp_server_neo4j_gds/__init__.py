import logging

from dotenv import load_dotenv

import argparse
import os


def main():
    """Main entry point for the package."""
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

    # Import and run the server directly without asyncio.run
    from .server import main as server_main

    server_main(
        db_url=args.db_url,
        username=args.username,
        password=args.password,
        database=args.database,
    )


__all__ = ["main"]
