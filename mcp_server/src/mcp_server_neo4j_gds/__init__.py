import logging
import os
import platform

from dotenv import load_dotenv

from . import server
import asyncio
import argparse


def get_log_file_path():
    """Get the appropriate log file path based on the environment."""
    current_dir = os.getcwd()

    # Check if we're in development (project directory has pyproject.toml or src/)
    if os.path.exists(os.path.join(current_dir, "pyproject.toml")) or os.path.exists(
        os.path.join(current_dir, "src")
    ):
        return "mcp-server-neo4j-gds.log"

    # Production: use platform-specific Claude logs directory
    system = platform.system()
    home = os.path.expanduser("~")

    if system == "Darwin":  # macOS
        claude_logs_dir = os.path.join(home, "Library", "Logs", "Claude")
    elif system == "Windows":
        claude_logs_dir = os.path.join(
            os.environ.get("APPDATA", home), "Claude", "Logs"
        )
    else:  # Linux and other Unix-like systems
        claude_logs_dir = os.path.join(home, ".local", "share", "Claude", "logs")

    # Use Claude logs directory if it exists, otherwise fall back to current directory
    if os.path.exists(claude_logs_dir):
        return os.path.join(claude_logs_dir, "mcp-server-neo4j-gds.log")
    else:
        return "mcp-server-neo4j-gds.log"


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

    log_file = get_log_file_path()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )

    logging.info(f"Starting MCP Server for {args.db_url} with username {args.username}")
    if args.database:
        logging.info(f"Connecting to database: {args.database}")
    asyncio.run(
        server.main(
            db_url=args.db_url,
            username=args.username,
            password=args.password,
            database=args.database,
        )
    )


__all__ = ["main", "server"]
