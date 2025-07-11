import pytest
import json


@pytest.mark.asyncio
async def test_find_shortest_path(mcp_client):
    """Test the find_shortest_path tool with real database and server."""

    # First, list available tools to ensure server is working
    tools = await mcp_client.list_tools()
    tool_names = [tool["name"] for tool in tools]
    assert "find_shortest_path" in tool_names

    # Test the shortest path between two known stations
    result = await mcp_client.call_tool(
        "find_shortest_path",
        {
            "start_node": "Canada Water",
            "end_node": "Tower Hill",
            "relationship_property": "time",
        },
    )

    # Parse the result (it comes as text content)
    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    # Verify the result structure
    assert "totalCost" in result_data
    assert "nodeIds" in result_data
    assert "nodeNames" in result_data

    # Verify the path starts and ends with the correct stations
    node_names = result_data["nodeNames"]
    assert len(node_names) > 0
    assert "Canada Water" in node_names[0]  # Using 'in' for partial matches
    assert "Tower Hill" in node_names[-1]

    # Verify the cost is positive
    assert result_data["totalCost"] > 0

    # Test with stations that should not have a path
    result = await mcp_client.call_tool(
        "find_shortest_path",
        {"start_node": "NonExistentStation1", "end_node": "NonExistentStation2"},
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    # For non-existent stations, we expect found to be False
    assert result_data["found"] is False
