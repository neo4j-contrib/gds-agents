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


@pytest.mark.asyncio
async def test_dijkstra_single_source_shortest_path(mcp_client):
    result = await mcp_client.call_tool(
        "dijkstra_single_source_shortest_path",
        {
            "sourceNode": "Canada Water",
            "nodeIdentifierProperty": "name",
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
        "dijkstra_single_source_shortest_path",
        {
            "sourceNode": "NonExistentStation",
            "nodeIdentifierProperty": "name",
        },
    )

    result_data = json.loads(result[0]["text"])
    assert result_data["found"] is False


@pytest.mark.asyncio
async def test_a_star_shortest_path(mcp_client):
    result = await mcp_client.call_tool(
        "a_star_shortest_path",
        {
            "sourceNode": "Canada Water",
            "targetNode": "Tower Hill",
            "nodeIdentifierProperty": "name",
            "relationshipWeightProperty": "time",
            "latitudeProperty": "latitude",
            "longitudeProperty": "longitude",
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
        "a_star_shortest_path",
        {
            "sourceNode": "NonExistentStation1",
            "targetNode": "NonExistentStation2",
            "nodeIdentifierProperty": "name",
            "latitudeProperty": "latitude",
            "longitudeProperty": "longitude",
        },
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data["found"] is False


@pytest.mark.asyncio
async def test_yens_shortest_paths(mcp_client):
    result = await mcp_client.call_tool(
        "yens_shortest_paths",
        {
            "sourceNode": "Canada Water",
            "targetNode": "Tower Hill",
            "nodeIdentifierProperty": "name",
            "relationshipWeightProperty": "time",
            "k": 3,
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert result_data["found"] is True
    assert "sourceNodeId" in result_data
    assert "targetNodeId" in result_data
    assert "sourceNodeName" in result_data
    assert "targetNodeName" in result_data
    assert "results" in result_data
    assert "totalResults" in result_data

    assert "Canada Water" in result_data["sourceNodeName"]
    assert "Tower Hill" in result_data["targetNodeName"]

    results = result_data["results"]
    assert 1 <= len(results) <= 3
    assert result_data["totalResults"] == len(results)

    first_result = results[0]
    assert "index" in first_result
    assert "totalCost" in first_result
    assert "nodeIds" in first_result
    assert "nodeNames" in first_result
    assert "costs" in first_result
    assert "path" in first_result

    # First path should be the optimal path (same as basic shortest path)
    assert first_result["totalCost"] == 9.0
    expected_node_ids = [292, 188, 243, 196, 261, 2, 230]
    assert first_result["nodeIds"] == expected_node_ids

    # Test with non-existent stations
    result = await mcp_client.call_tool(
        "yens_shortest_paths",
        {
            "sourceNode": "NonExistentStation1",
            "targetNode": "NonExistentStation2",
            "nodeIdentifierProperty": "name",
            "k": 2,
        },
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data["found"] is False


@pytest.mark.asyncio
async def test_minimum_weight_spanning_tree(mcp_client):
    result = await mcp_client.call_tool(
        "minimum_weight_spanning_tree",
        {
            "sourceNode": "Canada Water",
            "nodeIdentifierProperty": "name",
            "relationshipWeightProperty": "time",
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert result_data["found"] is True
    assert "totalWeight" in result_data
    assert "edges" in result_data

    edges = result_data["edges"]
    assert len(edges) == 301
    assert result_data["totalWeight"] > 0

    first_edge = edges[0]
    assert "nodeId" in first_edge
    assert "parentId" in first_edge
    assert "nodeName" in first_edge
    assert "parentName" in first_edge
    assert "weight" in first_edge
    assert first_edge["weight"] > 0

    # Test with non-existent source node
    result = await mcp_client.call_tool(
        "minimum_weight_spanning_tree",
        {
            "sourceNode": "NonExistentStation",
            "nodeIdentifierProperty": "name",
        },
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data["found"] is False


@pytest.mark.asyncio
async def test_minimum_directed_steiner_tree(mcp_client):
    result = await mcp_client.call_tool(
        "minimum_directed_steiner_tree",
        {
            "sourceNode": "Canada Water",
            "targetNodes": ["Tower Hill", "King's Cross St. Pancras", "London Bridge"],
            "nodeIdentifierProperty": "name",
            "relationshipWeightProperty": "time",
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert result_data["found"] is True
    assert "totalWeight" in result_data
    assert "edges" in result_data

    assert result_data["totalWeight"] > 0
    edges = result_data["edges"]
    assert len(edges) > 0

    first_edge = edges[0]
    assert "nodeId" in first_edge
    assert "parentId" in first_edge
    assert "weight" in first_edge
    assert first_edge["weight"] > 0

    # Test with non-existent source node
    result = await mcp_client.call_tool(
        "minimum_directed_steiner_tree",
        {
            "sourceNode": "NonExistentStation",
            "targetNodes": ["Tower Hill"],
            "nodeIdentifierProperty": "name",
        },
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data["found"] is False


@pytest.mark.asyncio
async def test_prize_collecting_steiner_tree(mcp_client):
    result = await mcp_client.call_tool(
        "prize_collecting_steiner_tree",
        {
            "relationshipWeightProperty": "time",
            "prizeProperty": "zone",
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert result_data["found"] is True
    assert "totalWeight" in result_data
    assert "edges" in result_data
    assert result_data["totalWeight"] > 0

    edges = result_data["edges"]
    assert len(edges) > 0

    first_edge = edges[0]
    assert "nodeId" in first_edge
    assert "parentId" in first_edge
    assert "weight" in first_edge
    assert first_edge["weight"] > 0


@pytest.mark.asyncio
async def test_all_pairs_shortest_paths(mcp_client):
    result = await mcp_client.call_tool(
        "all_pairs_shortest_paths",
        {
            "relationshipWeightProperty": "time",
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert result_data["found"] is True
    assert "paths" in result_data

    paths = result_data["paths"]
    assert len(paths) == 302 * 302

    first_path = paths[0]
    assert "sourceNodeId" in first_path
    assert "targetNodeId" in first_path
    assert "distance" in first_path

    distance = first_path["distance"]
    assert isinstance(distance, (int, float))
    assert distance >= 0 or distance == float("inf")
    finite_distances = [
        path["distance"] for path in paths if path["distance"] != float("inf")
    ]
    assert len(finite_distances) > 0  # Should have at least some connected node pairs


@pytest.mark.asyncio
async def test_random_walk(mcp_client):
    result = await mcp_client.call_tool(
        "random_walk",
        {
            "sourceNodes": ["Canada Water"],
            "nodeIdentifierProperty": "name",
            "walkLength": 5,
            "walksPerNode": 3,
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert result_data["found"] is True
    walks = result_data["walks"]
    assert len(walks) == 3

    # Test with no source nodes specified (should use all nodes)
    result = await mcp_client.call_tool(
        "random_walk",
        {
            "walkLength": 3,
            "walksPerNode": 1,
        },
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data["found"] is True

    walks = result_data["walks"]
    # Should have 302 walks (1 walk per node for 302 nodes)
    assert len(walks) == 302


@pytest.mark.asyncio
async def test_breadth_first_search(mcp_client):
    result = await mcp_client.call_tool(
        "breadth_first_search",
        {
            "sourceNode": "Canada Water",
            "nodeIdentifierProperty": "name",
            "maxDepth": 3,
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert result_data["found"] is True
    assert "traversals" in result_data

    traversals = result_data["traversals"]
    assert len(traversals) > 0

    first_traversal = traversals[0]
    assert "sourceNode" in first_traversal
    assert "nodeIds" in first_traversal
    assert "nodeNames" in first_traversal
    assert "visitedNodes" in first_traversal
    assert first_traversal["visitedNodes"] > 0
    assert "Canada Water" in first_traversal["nodeNames"][0]

    # Test with non-existent source node
    result = await mcp_client.call_tool(
        "breadth_first_search",
        {
            "sourceNode": "NonExistentStation",
            "nodeIdentifierProperty": "name",
        },
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data["found"] is False


@pytest.mark.asyncio
async def test_depth_first_search(mcp_client):
    result = await mcp_client.call_tool(
        "depth_first_search",
        {
            "sourceNode": "Canada Water",
            "nodeIdentifierProperty": "name",
            "maxDepth": 3,
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert result_data["found"] is True
    assert "traversals" in result_data

    traversals = result_data["traversals"]
    assert len(traversals) > 0

    first_traversal = traversals[0]
    assert "sourceNode" in first_traversal
    assert "nodeIds" in first_traversal
    assert "nodeNames" in first_traversal
    assert "visitedNodes" in first_traversal
    assert first_traversal["visitedNodes"] > 0
    assert "Canada Water" in first_traversal["nodeNames"][0]

    # Test with non-existent source node
    result = await mcp_client.call_tool(
        "depth_first_search",
        {
            "sourceNode": "NonExistentStation",
            "nodeIdentifierProperty": "name",
        },
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data["found"] is False


@pytest.mark.asyncio
async def test_bellman_ford_single_source_shortest_path(mcp_client):
    result = await mcp_client.call_tool(
        "bellman_ford_single_source_shortest_path",
        {
            "sourceNode": "Canada Water",
            "nodeIdentifierProperty": "name",
            "relationshipWeightProperty": "time",
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)

    assert result_data["found"] is True
    assert "paths" in result_data

    paths = result_data["paths"]
    assert len(paths) > 0

    first_path = paths[0]
    assert "index" in first_path
    assert "sourceNode" in first_path
    assert "targetNode" in first_path
    assert "totalCost" in first_path
    assert "nodeIds" in first_path
    assert "nodeNames" in first_path
    assert "costs" in first_path
    assert "isNegativeCycle" in first_path

    source_node_id = first_path["sourceNode"]
    for path in paths[:10]:  # Check first 10 paths
        assert path["sourceNode"] == source_node_id

    assert len(first_path["nodeIds"]) == len(first_path["nodeNames"])
    assert len(first_path["nodeIds"]) == len(first_path["costs"])
    assert "Canada Water" in first_path["nodeNames"][0]

    # Test with non-existent source node
    result = await mcp_client.call_tool(
        "bellman_ford_single_source_shortest_path",
        {
            "sourceNode": "NonExistentStation",
            "nodeIdentifierProperty": "name",
        },
    )

    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data["found"] is False


@pytest.mark.asyncio
async def test_longest_path(mcp_client):
    result = await mcp_client.call_tool(
        "longest_path",
        {
            "relationshipWeightProperty": "time",
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    result_data = json.loads(result_text)
    assert result_data == {
        "found": False,
        "message": "No longest paths found. The graph may contain cycles or be empty.",
    }
