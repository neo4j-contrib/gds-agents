from . import server
import asyncio
import argparse
import os


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='Neo4j GDS MCP Server')
    parser.add_argument('--db-url', 
                       default=os.environ.get("NEO4J_URI"),
                       help='URL to Neo4j database')
    parser.add_argument('--username', 
                       default=os.environ.get("NEO4J_USERNAME", "neo4j"),
                       help='Username for Neo4j database')
    parser.add_argument('--password', 
                       default=os.environ.get("NEO4J_PASSWORD"),
                       help='Password for Neo4j database')
    
    args = parser.parse_args()
    asyncio.run(server.main(db_url=args.db_url, username=args.username, password=args.password))


__all__ = ["main", "server"]
