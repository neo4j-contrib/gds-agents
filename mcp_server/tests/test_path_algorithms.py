import pytest
import json


@pytest.mark.asyncio
async def test_find_shortest_path(mcp_client):
    result = await mcp_client.call_tool(
        "find_shortest_path",
        {
            "start_node": "Canada Water",
            "end_node": "Tower Hill",
            "nodeIdentifierProperty": "name",
            "relationship_property": "time",
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert "nodeNames" in result_data
    assert result_data["totalCost"] == 9.0
    expected_node_ids = [292, 188, 243, 196, 261, 2, 230]
    assert result_data["nodeIds"] == expected_node_ids

    node_names = result_data["nodeNames"]
    assert len(node_names) == 7
    assert "Canada Water" in node_names[0]
    assert "Tower Hill" in node_names[-1]
    expected_stations = [
        "Canada Water",
        "Rotherhithe",
        "Wapping",
        "Shadwell",
        "Whitechapel",
        "Aldgate East",
        "Tower Hill",
    ]
    for i, expected_station in enumerate(expected_stations):
        assert expected_station in node_names[i]

    # Test with stations that should not have a path
    result = await mcp_client.call_tool(
        "find_shortest_path",
        {
            "start_node": "NonExistentStation1",
            "end_node": "NonExistentStation2",
            "nodeIdentifierProperty": "name",
        },
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data["found"] is False


@pytest.mark.asyncio
async def test_delta_stepping_shortest_path(mcp_client):
    result = await mcp_client.call_tool(
        "delta_stepping_shortest_path",
        {
            "sourceNode": "Canada Water",
            "nodeIdentifierProperty": "name",
            "delta": 2.0,
            "relationshipWeightProperty": "time",
        },
    )

    assert len(result) == 1
    result_data = json.loads(result[0]["text"])

    assert result_data["found"] is True
    assert "sourceNodeId" in result_data
    assert "sourceNodeName" in result_data
    assert "results" in result_data

    assert "Canada Water" in result_data["sourceNodeName"]

    results = result_data["results"]
    assert len(results) == 302
    # Verify structure of a result entry
    assert "targetNode" in results[42]
    assert "targetNodeName" in results[42]
    assert "totalCost" in results[42]
    assert "nodeIds" in results[42]
    assert "nodeNames" in results[42]
    assert "costs" in results[42]
    assert "path" in results[42]

    result = await mcp_client.call_tool(
        "delta_stepping_shortest_path",
        {
            "sourceNode": "NonExistentStation",
            "nodeIdentifierProperty": "name",
            "delta": 1.0,
        },
    )

    result_data = json.loads(result[0]["text"])
    assert result_data["found"] is False
