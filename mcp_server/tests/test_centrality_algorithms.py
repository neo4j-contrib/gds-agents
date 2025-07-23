import pytest


@pytest.mark.asyncio
async def test_article_rank(mcp_client):
    # Test basic
    baseline_result = await mcp_client.call_tool(
        "article_rank",
        {
            "nodeIdentifierProperty": "name",
            "dampingFactor": 0.85,
            "maxIterations": 20,
            "tolerance": 1e-6,
        },
    )

    assert len(baseline_result) == 1
    baseline_text = baseline_result[0]["text"]

    assert "nodeId" in baseline_text
    assert "score" in baseline_text
    assert "nodeName" in baseline_text

    baseline_lines = baseline_text.strip().split("\n")
    baseline_data_lines = [line for line in baseline_lines[1:] if line.strip()]
    assert len(baseline_data_lines) == 302

    # Test with node filtering
    result = await mcp_client.call_tool(
        "article_rank",
        {
            "nodeNames": ["Covent Garden", "Southwark"],
            "nodeIdentifierProperty": "name",
            "dampingFactor": 0.85,
        },
    )

    assert len(result) == 1
    result_text = result[0]["text"]
    assert "nodeId" in result_text
    assert "score" in result_text
    assert "nodeName" in result_text

    lines = result_text.strip().split("\n")
    data_lines = [line for line in lines[1:] if line.strip()]
    assert len(data_lines) <= 2  # Should not exceed the number of filtered nodes

    # Test basic (no node names)
    basic_result = await mcp_client.call_tool(
        "article_rank",
        {
            "dampingFactor": 0.85,
        },
    )

    assert len(basic_result) == 1
    basic_text = basic_result[0]["text"]

    assert "nodeId" in basic_text
    assert "score" in basic_text
    assert "nodeName" not in basic_text

    # Test personalized article rank with sourceNodes
    personalized_result = await mcp_client.call_tool(
        "article_rank",
        {
            "sourceNodes": ["Covent Garden", "Southwark"],
            "nodeIdentifierProperty": "name",
            "dampingFactor": 0.85,
            "maxIterations": 20,
        },
    )

    assert len(personalized_result) == 1
    personalized_text = personalized_result[0]["text"]
    assert "nodeId" in personalized_text
    assert "score" in personalized_text
    assert "nodeName" in personalized_text

    personalized_lines = personalized_text.strip().split("\n")
    personalized_data_lines = [line for line in personalized_lines[1:] if line.strip()]
    assert len(personalized_data_lines) == 302

    # Extract scores for source nodes from both baseline and personalized results
    # to verify that personalization is working
    def extract_score_for_station(text, station_name):
        lines = text.strip().split("\n")
        for line in lines[1:]:
            if station_name in line:
                import re

                parts = re.split(r"\s+", line.strip())
                if len(parts) >= 3:
                    try:
                        score_candidates = []
                        for i in range(1, min(4, len(parts))):
                            try:
                                score_candidates.append((i, float(parts[i])))
                            except ValueError:
                                continue

                        if len(score_candidates) >= 2:
                            return score_candidates[1][1]
                        elif len(score_candidates) >= 1:
                            return score_candidates[0][1]
                    except (ValueError, IndexError):
                        continue
        return None

    print("DEBUG - Baseline first 3 lines:")
    baseline_lines_debug = baseline_text.strip().split("\n")[:3]
    for i, line in enumerate(baseline_lines_debug):
        print(f"  {i}: {repr(line)}")

    print("DEBUG - Personalized first 3 lines:")
    personalized_lines_debug = personalized_text.strip().split("\n")[:3]
    for i, line in enumerate(personalized_lines_debug):
        print(f"  {i}: {repr(line)}")

    # Check that personalized scores are different from baseline for source nodes
    baseline_cg_score = extract_score_for_station(baseline_text, "Covent Garden")
    personalized_cg_score = extract_score_for_station(
        personalized_text, "Covent Garden"
    )

    baseline_sw_score = extract_score_for_station(baseline_text, "Southwark")
    personalized_sw_score = extract_score_for_station(personalized_text, "Southwark")

    assert baseline_cg_score is not None and personalized_cg_score is not None
    assert baseline_sw_score is not None and personalized_sw_score is not None
    cg_diff = abs(baseline_cg_score - personalized_cg_score)
    sw_diff = abs(baseline_sw_score - personalized_sw_score)

    assert cg_diff > 0.001, (
        f"Personalized ArticleRank should change scores for Covent Garden (diff: {cg_diff})"
    )
    assert sw_diff > 0.001, (
        f"Personalized ArticleRank should change scores for Southwark (diff: {sw_diff})"
    )

    # Test combining sourceNodes with nodeNames filtering
    combined_result = await mcp_client.call_tool(
        "article_rank",
        {
            "sourceNodes": ["Covent Garden"],
            "nodeNames": ["Covent Garden", "Southwark", "London Bridge"],
            "nodeIdentifierProperty": "name",
            "dampingFactor": 0.85,
        },
    )

    assert len(combined_result) == 1
    combined_text = combined_result[0]["text"]

    assert "nodeId" in combined_text
    assert "score" in combined_text
    assert "nodeName" in combined_text

    combined_lines = combined_text.strip().split("\n")
    combined_data_lines = [line for line in combined_lines[1:] if line.strip()]
    assert len(combined_data_lines) <= 3

    combined_full_text = " ".join(combined_data_lines)
    assert (
        "Covent Garden" in combined_full_text
        and "Southwark" in combined_full_text
        and "London Bridge" in combined_full_text
    )
