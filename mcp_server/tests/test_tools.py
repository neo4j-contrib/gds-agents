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
async def test_count_nodes(mcp_client):
    result = await mcp_client.call_tool("count_nodes")

    assert len(result) == 1
    result_text = result[0]["text"]
    node_count = int(result_text.strip())
    assert node_count == 302


@pytest.mark.asyncio
async def test_list_tools(mcp_client):
    """Test that all expected tools are listed."""

    # Get list of available tools
    tools = await mcp_client.list_tools()
    tool_names = [tool["name"] for tool in tools]

    # Expected tools (based on server.py imports)
    expected_tools = [
        # Basic tools
        "count_nodes",
        "get_node_properties_keys",
        # Centrality algorithms
        "article_rank",
        "articulation_points",
        "betweenness_centrality",
        "bridges",
        "CELF",
        "closeness_centrality",
        "degree_centrality",
        "eigenvector_centrality",
        "pagerank",
        "harmonic_centrality",
        "HITS",
        # Community algorithms
        "conductance",
        "HDBSCAN",
        "k_core_decomposition",
        "k_1_coloring",
        "k_means_clustering",
        "label_propagation",
        "leiden",
        "local_clustering_coefficient",
        "louvain",
        "modularity_metric",
        "modularity_optimization",
        "strongly_connected_components",
        "triangle_count",
        "weakly_connected_components",
        "approximate_maximum_k_cut",
        "speaker_listener_label_propagation",
        # Path algorithms
        "find_shortest_path",
        "delta_stepping_shortest_path",
        "dijkstra_single_source_shortest_path",
        "a_star_shortest_path",
        "yens_shortest_paths",
        "minimum_weight_spanning_tree",
        "minimum_weight_k_spanning_tree",
        "minimum_directed_steiner_tree",
        "prize_collecting_steiner_tree",
        "all_pairs_shortest_paths",
        "random_walk",
        "breadth_first_search",
        "depth_first_search",
        "bellman_ford_single_source_shortest_path",
        "longest_path",
    ]

    # Check that we have the expected tools
    assert len(tool_names) == len(expected_tools)
    for expected_tool in expected_tools:
        assert expected_tool in tool_names, (
            f"Expected tool '{expected_tool}' not found in tool list"
        )
