from mcp import types

community_tool_definitions = [
    types.Tool(
        name="conductance",
        description="""Calculate the conductance metric for all communities""",
        inputSchema={
            "type": "object",
            "properties": {
                "communityProperty": {
                    "type": "string",
                    "description": "The node property that holds the community ID as an integer for each node. "
                                   "Note that only non-negative community IDs are considered valid and will have their conductance computed."
                },
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "The relationship property that holds the weight of the relationships. "
                                   "If not provided, all relationships are considered to have a weight of 1."
                }
            },
            "required": ["communityProperty"]
        }
    ),
    types.Tool(
        name="HDBSCAN",
        description="Perform HDBSCAN clustering on the graph. HDBSCAN, which stands for Hierarchical Density-Based Spatial Clustering of Applications with Noise, "
                    "is a clustering algorithm used to identify clusters of similar data points within a dataset. "
                    "It builds upon the DBSCAN algorithm but adds a hierarchical structure, making it more robust to varying densities within the data. "
                    "Unlike DBSCAN, HDBSCAN does not require tuning a specific density parameter; "
                    "instead, it runs DBSCAN over a range of parameters, creating a hierarchy of clusters. "
                    "This hierarchical approach allows HDBSCAN to find clusters of varying densities and to be more adaptable to real-world data.HDBSCAN is known for its ease of use, "
                    "noise tolerance, and ability to handle data with varying densities, making it a versatile tool for clustering tasks, "
                    "especially when dealing with complex, high-dimensional datasets.",
        inputSchema={
            "type": "object",
            "properties": {
                "nodeProperty": {
                    "type": "string",
                    "description": "A node property corresponding to an array of floats used by HDBSCAN to compute clusters"
                },
                "minClusterSize": {
                    "type": "integer",
                    "description": "The minimum number of nodes that a cluster should contain."
                },
                "samples": {
                    "type": "integer",
                    "description": "The number of neighbours to be considered when computing the core distances of a node."
                },
                "leafSize": {
                    "type": "integer",
                    "description": "The number of leaf nodes of the supporting tree data structure."
                }
            },
            "required": ["nodeProperty"]
        }
    ),
    types.Tool(
        name="k-core decomposition",
        description="The K-core decomposition constitutes a process of separates the nodes in a graph into groups based on the degree sequence and topology of the graph. "
        "The term i-core refers to a maximal subgraph of the original graph such that each node in this subgraph has degree at least i. "
        "The maximality ensures that it is not possible to find another subgraph with more nodes where this degree property holds. "
        "The nodes in the subgraph denoted by i-core also belong to the subgraph denoted by j-core for any j<i. The converse however is not true.  "
        "Each node u is associated with a core value which denotes the largest value i such that u belongs to the i-core. "
        "The largest core value is called the degeneracy of the graph.Standard algorithms for K-Core Decomposition iteratively remove the node of lowest degree until the graph becomes empty. "
        "When a node is removed from the graph, all of its relationships are removed, and the degree of its neighbors is reduced by one. "
        "With this approach, the different core groups are discovered one-by-one.",
        inputSchema={
            "type": "object",
        }
    ),
    types.Tool(
        name="k-1 coloring",
        description="The K-1 Coloring algorithm assigns a color to every node in the graph, "
                    "trying to optimize for two objectives: "
                    "1. To make sure that every neighbor of a given node has a different color than the node itself. "
                    "2. To use as few colors as possible. "
                    "Note that the graph coloring problem is proven to be NP-complete, which makes it intractable on anything but trivial graph sizes. "
                    "For that reason the implemented algorithm is a greedy algorithm. "
                    "Thus it is neither guaranteed that the result is an optimal solution, using as few colors as theoretically possible, "
                    "nor does it always produce a correct result where no two neighboring nodes have different colors. "
                    "However the precision of the latter can be controlled by the number of iterations this algorithm runs.",
        inputSchema={
            "type": "object",
            "properties": {
                "maxIterations": {
                    "type": "integer",
                    "description": "The maximum number of iterations to run the coloring algorithm.",
                },
                "minCommunitySize": {
                    "type": "integer",
                    "description": "Only nodes inside communities larger or equal the given value are returned.",
                }
            }
        }
    ),
    types.Tool(
        name="k-means clustering",
        description="K-Means clustering is an unsupervised learning algorithm that is used to solve clustering problems. "
                   "It follows a simple procedure of classifying a given data set into a number of clusters, defined by the parameter k. "
                   "The Neo4j GDS Library conducts clustering based on node properties, with a float array node property being passed as input via the nodeProperty parameter. "
                   "Nodes in the graph are then positioned as points in a d-dimensional space (where d is the length of the array property). "
                   "The algorithm then begins by selecting k initial cluster centroids, which are d-dimensional arrays (see section below for more details). "
                   "The centroids act as representatives for a cluster. "
                   "Then, all nodes in the graph calculate their Euclidean distance from each of the cluster centroids and are assigned to the cluster of minimum distance from them. "
                   "After these assignments, each cluster takes the mean of all nodes (as points) assigned to it to form its new representative centroid (as a d-dimensional array). "
                   "The process repeats with the new centroids until results stabilize, i.e., only a few nodes change clusters per iteration or the number of maximum iterations is reached. "
                   "Note that the K-Means implementation ignores relationships as it is only focused on node properties.",
        inputSchema={
            "type": "object",
            "properties": {
                "nodeProperty": {
                    "type": "string",
                    "description": "A node property corresponding to an array of floats used by K-Means to cluster nodes into communities."
                },
                "k": {
                    "type": "integer",
                    "description": "The number of clusters to create."
                },
                "maxIterations": {
                    "type": "integer",
                    "description": "The maximum number of iterations the algorithm will run."
                },
                "deltaThreshold": {
                    "type": "number",
                    "description": "Value as a percentage to determine when to stop early. If fewer than 'deltaThreshold * |nodes|' nodes change their cluster , the algorithm stops. Value must be between 0 (exclusive) and 1 (inclusive)."
                },
                "numberOfRestarts": {
                    "type": "integer",
                    "description": "Number of times to execute K-Means with different initial centers. The communities returned are those minimizing the average node-center distances."
                },
                "initialSampler": {
                    "type": "string",
                    "enum": ["uniform", "kmeans++"],
                    "description": "The method used to sample the first k centroids. 'uniform' and 'kmeans++', both case-insensitive, are valid inputs."
                },
                "seedCentroids": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    },
                    "description": "Parameter to explicitly give the initial centroids. It cannot be enabled together with a non-default value of the numberOfRestarts parameter."
                },
                "computeSilhouette": {
                    "type": "boolean",
                    "description": "If set to true, the silhouette scores are computed once the clustering has been determined. Silhouette is a metric on how well the nodes have been clustered."
                }
            },
            "required": ["nodeProperty"]
        }
    ),
    types.Tool(
        name="label propagation",
        description="The Label Propagation algorithm (LPA) is a fast algorithm for finding communities in a graph. "
                   "It detects these communities using network structure alone as its guide, and doesn't require a pre-defined objective function or prior information about the communities. "
                   "LPA works by propagating labels throughout the network and forming communities based on this process of label propagation.",
        inputSchema={
            "type": "object",
            "properties": {
                "maxIterations": {
                    "type": "integer",
                    "description": "The maximum number of iterations to run.",
                },
                "nodeWeightProperty": {
                    "type": "string",
                    "description": "The name of a node property that contains node weights."
                },
                "relationshipWeightProperty": {
                    "type": "string",
                    "description": "Name of the relationship property to use as weights. If unspecified, the algorithm runs unweighted."
                },
                "seedProperty": {
                    "type": "string",
                    "description": "The name of a node property that defines an initial numeric label.",
                },
                "consecutiveIds": {
                    "type": "boolean",
                    "description": "Flag to decide whether component identifiers are mapped into a consecutive id space (requires additional memory).",
                },
                "minCommunitySize": {
                    "type": "integer",
                    "description": "Only nodes inside communities larger or equal the given value are returned.",
                }
            }
        }
    ),
    types.Tool(
        name="leiden",
        description="The Leiden algorithm is an algorithm for detecting communities in large networks. "
                   "The algorithm separates nodes into disjoint communities so as to maximize a modularity score for each community. "
                   "Modularity quantifies the quality of an assignment of nodes to communities, that is how densely connected nodes in a community are, compared to how connected they would be in a random network. "
                   "The Leiden algorithm is a hierarchical clustering algorithm, that recursively merges communities into single nodes by greedily optimizing the modularity and the process repeats in the condensed graph. "
                   "It modifies the Louvain algorithm to address some of its shortcomings, namely the case where some of the communities found by Louvain are not well-connected. "
                   "This is achieved by periodically randomly breaking down communities into smaller well-connected ones.",
        inputSchema={
            "type": "object",
            "properties": {
                "maxLevels": {
                    "type": "integer",
                    "description": "The maximum number of levels in which the graph is clustered and then condensed.",
                },
                "gamma": {
                    "type": "number",
                    "description": "Resolution parameter used when computing the modularity. Internally the value is divided by the number of relationships for an unweighted graph, or the sum of weights of all relationships otherwise.",
                },
                "theta": {
                    "type": "number",
                    "description": "Controls the randomness while breaking a community into smaller ones.",
                },
                "tolerance": {
                    "type": "number",
                    "description": "Minimum change in modularity between iterations. If the modularity changes less than the tolerance value, the result is considered stable and the algorithm returns.",
                },
                "includeIntermediateCommunities": {
                    "type": "boolean",
                    "description": "Indicates whether to write intermediate communities. If set to false, only the final community is persisted.",
                },
                "seedProperty": {
                    "type": "string",
                    "description": "Used to set the initial community for a node. The property value needs to be a non-negative number."
                },
                "minCommunitySize": {
                    "type": "integer",
                    "description": "Only nodes inside communities larger or equal the given value are returned.",
                }
            }
        }
    )
]