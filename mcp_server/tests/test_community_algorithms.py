import pytest


@pytest.mark.asyncio
async def test_conductance(mcp_client):
    result = await mcp_client.call_tool(
        "conductance", {"communityProperty": "total_lines"}
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    assert "community" in result_text
    assert "conductance" in result_text
    lines = result_text.strip().split("\n")
    data_lines = [line for line in lines[1:] if line.strip()]
    assert len(data_lines) > 0


@pytest.mark.asyncio
async def test_hdbscan(mcp_client):
    # TODO: Implement test for HDBSCAN. The LN-Underground graph does not have an array node property to use for clustering.
    pass


@pytest.mark.asyncio
async def test_k_core_decomposition(mcp_client):
    result_with_names = await mcp_client.call_tool(
        "k_core_decomposition", {"nodeIdentifierProperty": "name"}
    )

    assert len(result_with_names) == 1
    result_with_names_text = result_with_names[0]["text"]
    assert "nodeId" in result_with_names_text
    assert "coreValue" in result_with_names_text
    assert "nodeName" in result_with_names_text
    lines = result_with_names_text.strip().split("\n")
    data_lines = [line for line in lines[1:] if line.strip()]
    assert len(data_lines) > 0


@pytest.mark.asyncio
async def test_k_1_coloring(mcp_client):
    result_with_names = await mcp_client.call_tool(
        "k_1_coloring", {"nodeIdentifierProperty": "name", "maxIterations": 5}
    )

    assert len(result_with_names) == 1
    result_with_names_text = result_with_names[0]["text"]
    assert "nodeId" in result_with_names_text
    assert "color" in result_with_names_text
    assert "nodeName" in result_with_names_text
    lines = result_with_names_text.strip().split("\n")
    data_lines = [line for line in lines[1:] if line.strip()]
    assert len(data_lines) > 0


@pytest.mark.asyncio
async def test_k_means_clustering(mcp_client):
    # TODO: Implement test for K-Means Clustering. The LN-Underground graph does not have an array node property to use for clustering.
    pass
