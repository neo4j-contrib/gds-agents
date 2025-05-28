from mcp import types

centrality_tool_definitions = [
    types.Tool(
        name="article_rank",
        description="""Calculate ArticleRank for nodes in the graph. 
    ArticleRank is similar to PageRank but normalizes by the number of outgoing references.""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {"type": "array", "items": {"type": "string"},
                          "description": "List of nodes to return the ArticleRank for."},
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes."
                },
                "dampingFactor": {"type": "number",
                                  "description": "The damping factor of the ArticleRank calculation. Must be in [0, 1)."},
                "maxIterations": {"type": "integer", "description": "Maximum number of iterations for ArticleRank"},
                "tolerance": {"type": "number", "description": "Minimum change in scores between iterations."},
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "Property of the relationship to use for weighting. If not specified, all relationships are treated equally."
                },
                # The signature takes node "names" STRING instead of nodeIds according to GDS doc.
                # The "names" need to be resolved to actual nodes, using the property_key.
                "sourceNodes": {
                    "description": "The nodes or node ids or node-bias pairs to use for computing Personalized Article Rank. To use different bias for different source nodes, use the syntax: [[node1, bias1], [node2, bias2], ...]",
                    "anyOf": [
                        {
                            "type": "string",
                            "description": "Single node"
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of nodes"
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "prefixItems": [
                                    {"type": "string"},
                                    {"type": "number"}
                                ],
                                "minItems": 2,
                                "maxItems": 2
                            },
                            "description": "List of [node, bias] pairs"
                        }
                    ]
                },
                "scaler": {
                    "type": "string",
                    "description": "The name of the scaler applied for the final scores. "
                                   "Supported values are None, MinMax, Max, Mean, Log, and StdScore. "
                                   "To apply scaler-specific configuration, use the Map syntax: {scaler: 'name', ...}."
                },
            },
            "required": [],
        },
    ),
    types.Tool(
        name="degree_centrality",
        description="""Calculate degree centrality for all nodes in the graph""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {"type": "array", "items": {"type": "string"},
                          "description": "List of nodes to return the centrality for"},
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes."
                }
            },
            "required": [],
        },
    ),
    types.Tool(
        name="pagerank",
        description="""Calculate PageRank for all nodes in the graph""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {"type": "array", "items": {"type": "string"},
                          "description": "List of nodes to return the PageRank for."},
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes."
                },
                "dampingFactor": {"type": "number",
                                  "description": "The damping factor of the Page Rank calculation. Must be in [0, 1)."},
                "maxIterations": {"type": "integer", "description": "Maximum number of iterations for PageRank"},
                "tolerance": {"type": "number",
                              "description": "Minimum change in scores between iterations. If all scores change less than the tolerance value the result is considered stable and the algorithm returns."}
            },
            "required": [],
        },
    ),
]