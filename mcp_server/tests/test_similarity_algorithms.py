import pytest


@pytest.mark.asyncio
async def test_node_similarity(mcp_client):
    result = await mcp_client.call_tool(
        "node_similarity", {"nodeIdentifierProperty": "name", "topN": 35}
    )

    assert len(result) == 1

    result_text = result[0]["text"]

    # Verify structure of a result entry
    assert "node1" in result_text
    assert "node2" in result_text
    assert "node1Name" in result_text
    assert "node2Name" in result_text
    assert "similarity" in result_text
    lines = result_text.strip().split("\n")
    data_lines = [line for line in lines[1:] if line.strip()]
    assert len(data_lines) == 35
    assert "Aldgate" in data_lines[34]


@pytest.mark.asyncio
async def test_filtered_node_similarity(mcp_client):
    # test source-filter only
    result = await mcp_client.call_tool(
        "filtered_node_similarity",
        {
            "nodeIdentifierProperty": "name",
            "topK": 3,
            "sourceNodeFilter": ["Acton Town"],
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    # Verify structure of a result entry
    assert "node1" in result_text
    assert "node2" in result_text
    assert "node1Name" in result_text
    assert "node2Name" in result_text
    assert "similarity" in result_text
    lines = result_text.strip().split("\n")
    data_lines = [line for line in lines[1:] if line.strip()]
    assert len(data_lines) == 3
    assert "Acton Town" in data_lines[0]

    # test target-filter alone

    result = await mcp_client.call_tool(
        "filtered_node_similarity",
        {
            "nodeIdentifierProperty": "name",
            "topK": 3,
            "targetNodeFilter": "Stamford Brook",
        },
    )
    assert len(result) == 1
    result_text = result[0]["text"]
    # Verify structure of a result entry
    assert "node1" in result_text
    assert "node2" in result_text
    assert "node1Name" in result_text
    assert "node2Name" in result_text
    assert "similarity" in result_text
    lines = result_text.strip().split("\n")
    data_lines = [line for line in lines[1:] if line.strip()]
    assert len(data_lines) == 4
    assert "Stamford Brook" in data_lines[0]

    # test combination of filters
    result = await mcp_client.call_tool(
        "filtered_node_similarity",
        {
            "nodeIdentifierProperty": "name",
            "topK": 3,
            "sourceNodeFilter": ["Acton Town"],
            "targetNodeFilter": ["Stamford Brook"],
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    # Verify structure of a result entry
    assert "node1" in result_text
    assert "node2" in result_text
    assert "node1Name" in result_text
    assert "node2Name" in result_text
    assert "similarity" in result_text
    lines = result_text.strip().split("\n")
    data_lines = [line for line in lines[1:] if line.strip()]
    assert len(data_lines) == 1
    assert "Acton Town" in data_lines[0]
    assert "Stamford Brook" in data_lines[0]
