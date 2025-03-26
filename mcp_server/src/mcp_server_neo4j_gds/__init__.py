from . import server
import asyncio
import argparse


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='Neo4j GDS MCP Server')
    parser.add_argument('--db-url', 
                       default="neo4j+s://57327d08.databases.neo4j.io",
                       help='URL to Neo4j database')
    parser.add_argument('--username', 
                       default="neo4j",
                       help='Username for Neo4j database')
    parser.add_argument('--password', 
                       help='Password for Neo4j database')
    
    args = parser.parse_args()
    asyncio.run(server.main(db_url=args.db_url, username=args.username, password=args.password))


__all__ = ["main", "server"]
