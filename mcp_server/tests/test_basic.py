import pytest
import asyncio
import json
import os
from dotenv import load_dotenv
from fastmcp import Client


@pytest.fixture
def mcp_server():
    """Create a FastMCP server instance using the actual server setup"""
    # Load environment variables
    load_dotenv("../../../.env")

    # Import the actual server setup function
    from mcp_server_neo4j_gds.server import setup_server

    # Get environment variables
    db_url = os.environ.get("NEO4J_URI")
    username = os.environ.get("NEO4J_USERNAME", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD")
    database = os.environ.get("NEO4J_DATABASE")

    # Use the actual server setup function
    server = setup_server(db_url, username, password, database)

    return server


@pytest.mark.asyncio
async def test_find_shortest_path(mcp_server):
    """Test the find_shortest_path tool with correct parameters using the actual server"""
    # Pass the server directly to the Client constructor for in-memory testing
    async with Client(mcp_server) as client:
        # Test the find_shortest_path tool with correct parameter names
        result = await client.call_tool(
            "find_shortest_path", {"start_node": "Tower Hill", "end_node": "Paddington"}
        )

        # Parse the result
        result_data = json.loads(result.data)
        breakpoint()

        # Assertions
        assert "totalCost" in result_data, "Result should contain totalCost"
        assert "nodeIds" in result_data, "Result should contain nodeIds"
        assert "nodeNames" in result_data, "Result should contain nodeNames"
        assert "path" in result_data, "Result should contain path"
        assert "costs" in result_data, "Result should contain costs"

        # Check that we got a valid path
        assert result_data["totalCost"] > 0, "Total cost should be positive"
        assert len(result_data["nodeIds"]) > 0, "Should have at least one node in path"
        assert len(result_data["nodeNames"]) > 0, "Should have at least one node name"

        print(f"✅ find_shortest_path test passed!")
        print(
            f"Path from {result_data['nodeNames'][0]} to {result_data['nodeNames'][-1]}"
        )
        print(f"Total cost: {result_data['totalCost']}")
        print(f"Number of nodes: {len(result_data['nodeIds'])}")


if __name__ == "__main__":
    asyncio.run(test_find_shortest_path())
