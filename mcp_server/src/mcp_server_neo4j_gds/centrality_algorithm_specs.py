from mcp import types

centrality_tool_definitions = [
    types.Tool(
        name="article_rank",
        description="""Calculate ArticleRank for nodes in the graph. 
    ArticleRank is similar to PageRank but normalizes by the number of outgoing references.""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of nodes to return the ArticleRank for.",
                },
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes.",
                },
                "dampingFactor": {
                    "type": "number",
                    "description": "The damping factor of the ArticleRank calculation. Must be in [0, 1).",
                },
                "maxIterations": {
                    "type": "integer",
                    "description": "Maximum number of iterations for ArticleRank",
                },
                "tolerance": {
                    "type": "number",
                    "description": "Minimum change in scores between iterations.",
                },
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "Property of the relationship to use for weighting. If not specified, all relationships are treated equally.",
                },
                # The signature takes node "names" STRING instead of nodeIds according to GDS doc.
                # The "names" need to be resolved to actual nodes, using the property_key.
                "sourceNodes": {
                    "description": "The nodes or node ids or node-bias pairs to use for computing Personalized Article Rank. To use different bias for different source nodes, use the syntax: [[node1, bias1], [node2, bias2], ...]",
                    "anyOf": [
                        {"type": "string", "description": "Single node"},
                        {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of nodes",
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "prefixItems": [{"type": "string"}, {"type": "number"}],
                                "minItems": 2,
                                "maxItems": 2,
                            },
                            "description": "List of [node, bias] pairs",
                        },
                    ],
                },
                "scaler": {
                    "type": "string",
                    "description": "The name of the scaler applied for the final scores. "
                    "Supported values are None, MinMax, Max, Mean, Log, and StdScore. "
                    "To apply scaler-specific configuration, use the Map syntax: {scaler: 'name', ...}.",
                },
            },
            "required": [],
        },
    ),
    types.Tool(
        name="articulation_points",
        description="Find all the articulation points. Given a graph, an articulation point is a node whose removal increases the number of connected components in the graph.",
        inputSchema={
            "type": "object",
        },
    ),
    types.Tool(
        name="betweenness_centrality",
        description="""Calculate betweenness centrality for nodes in the graph.  Betweenness centrality is a measure of the number of times a node acts as a bridge along the shortest path between two other nodes.""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of nodes to return the betweenness centrality for.",
                },
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes.",
                },
                "samplingSize": {
                    "type": "integer",
                    "description": "The number of source nodes to consider for computing centrality scores.",
                },
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "Property of the relationship to use for weighting. If not specified, all relationships are treated equally.",
                },
            },
            "required": [],
        },
    ),
    types.Tool(
        name="bridges",
        description="""Find all the bridges in the graph. A bridge is an edge whose removal increases the number of connected components in the graph.""",
        inputSchema={
            "type": "object",
        },
    ),
    types.Tool(
        name="CELF",
        description="""Calculate the Cost-Effective Lazy Forward (CELF) algorithm for influence maximization in the graph. 
        For a given k, the algorithm finds the set of k nodes that maximize the expected spread of influence in the network.""",
        inputSchema={
            "type": "object",
            "properties": {
                "seedSetSize": {
                    "type": "integer",
                    "description": "The number of nodes that maximize the expected spread in the network.",
                },
                "monteCarloSimulations": {
                    "type": "integer",
                    "description": "The number of Monte Carlo simulations to run for estimating the expected spread.",
                },
                "propagationProbability": {
                    "type": "number",
                    "description": "The probability of propagating influence from a node to its neighbors.",
                },
            },
            "required": ["seedSetSize"],
        },
    ),
    types.Tool(
        name="closeness_centrality",
        description="""Calculate closeness centrality for all nodes in the graph. 
        The closeness centrality of a node measures its average farness (inverse distance) to all other nodes. 
        Nodes with a high closeness score have the shortest distances to all other nodes.""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of nodes to return the closeness centrality for.",
                },
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes.",
                },
                "useWassermanFaust": {
                    "type": "boolean",
                    "description": "If true, uses the Wasserman-Faust formula for closeness centrality. ",
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
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of nodes to return the centrality for",
                },
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes.",
                },
            },
            "required": [],
        },
    ),
    types.Tool(
        name="eigenvector_centrality",
        description="""Calculate eigenvector centrality for all nodes in the graph. 
    Eigenvector Centrality is an algorithm that measures the transitive influence of nodes. 
    Relationships originating from high-scoring nodes contribute more to the score of a node than connections from low-scoring nodes. 
    A high eigenvector score means that a node is connected to many nodes who themselves have high scores.
    The algorithm computes the eigenvector associated with the largest absolute eigenvalue. 
    To compute that eigenvalue, the algorithm applies the power iteration approach. 
    Within each iteration, the centrality score for each node is derived from the scores of its incoming neighbors. 
    In the power iteration method, the eigenvector is L2-normalized after each iteration, leading to normalized results by default. 
    The PageRank algorithm is a variant of Eigenvector Centrality with an additional jump probability.""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of nodes to return the eigenvector centrality for.",
                },
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes.",
                },
                "maxIterations": {
                    "type": "integer",
                    "description": "Maximum number of iterations for Eigenvector Centrality",
                },
                "tolerance": {
                    "type": "number",
                    "description": "Minimum change in scores between iterations. If all scores change less than the tolerance value the result is considered stable and the algorithm returns.",
                },
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "Property of the relationship to use for weighting. If not specified, all relationships are treated equally.",
                },
                # The signature takes node "names" STRING instead of nodeIds according to GDS doc.
                # The "names" need to be resolved to actual nodes, using the property_key.
                "sourceNodes": {
                    "description": "The nodes or node ids or node-bias pairs to use for computing Personalized Article Rank. To use different bias for different source nodes, use the syntax: [[node1, bias1], [node2, bias2], ...]",
                    "anyOf": [
                        {"type": "string", "description": "Single node"},
                        {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of nodes",
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "prefixItems": [{"type": "string"}, {"type": "number"}],
                                "minItems": 2,
                                "maxItems": 2,
                            },
                            "description": "List of [node, bias] pairs",
                        },
                    ],
                },
                "scaler": {
                    "type": "string",
                    "description": "The name of the scaler applied for the final scores. "
                    "Supported values are None, MinMax, Max, Mean, Log, and StdScore. "
                    "To apply scaler-specific configuration, use the Map syntax: {scaler: 'name', ...}.",
                },
            },
        },
    ),
    types.Tool(
        name="pagerank",
        description="""Calculate PageRank for all nodes in the graph""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of nodes to return the PageRank for.",
                },
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes.",
                },
                "dampingFactor": {
                    "type": "number",
                    "description": "The damping factor of the Page Rank calculation. Must be in [0, 1).",
                },
                "maxIterations": {
                    "type": "integer",
                    "description": "Maximum number of iterations for PageRank",
                },
                "tolerance": {
                    "type": "number",
                    "description": "Minimum change in scores between iterations. If all scores change less than the tolerance value the result is considered stable and the algorithm returns.",
                },
            },
            "required": [],
        },
    ),
    types.Tool(
        name="harmonic_centrality",
        description="""Calculate harmonic centrality for all nodes in the graph.
        Harmonic centrality is a variant of closeness centrality that is more robust to disconnected graphs.""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of nodes to return the harmonic centrality for.",
                },
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes.",
                },
            },
            "required": [],
        },
    ),
    types.Tool(
        name="HITS",
        description="""Calculate HITS (Hyperlink-Induced Topic Search) scores for nodes in the graph. 
        The Hyperlink-Induced Topic Search (HITS) is a link analysis algorithm that rates nodes based on two scores, a hub score and an authority score. 
        The authority score estimates the importance of the node within the network. The hub score estimates the value of its relationships to other nodes.""",
        inputSchema={
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of nodes to return the HITS scores for.",
                },
                "property_key": {
                    "type": "string",
                    "description": "Property key to use to filter the specified nodes.",
                },
                "hitsIterations": {
                    "type": "integer",
                    "description": "The number of hits iterations to run. The number of pregel iterations will be equal to hitsIterations * 4.",
                },
                "authProperty": {
                    "type": "string",
                    "description": "The name of the auth property to use.",
                },
                "hubProperty": {
                    "type": "string",
                    "description": "The name of the hub property to use.",
                },
                "partitioning": {
                    "type": "string",
                    "enum": ["AUTO", "RANGE", "DEGREE"],
                    "description": "The partitioning scheme used to divide the work between threads. Available options are AUTO, RANGE, DEGREE.",
                },
            },
            "required": [],
        },
    ),
]
