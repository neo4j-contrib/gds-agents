from graphdatascience import GraphDataScience


def count_nodes(db_url: str, username: str, password: str):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=True)
    
    # Get node count directly using Cypher
    node_count_query = "MATCH (n) RETURN count(n) as count"
    node_count_result = gds.run_cypher(node_count_query)
    node_count = node_count_result.iloc[0]['count']
    
    # Get all node labels from the database
    node_labels_query = "CALL db.labels()"
    node_labels = gds.run_cypher(node_labels_query).values.flatten().tolist()
    
    # Get all relationship types from the database
    rel_types_query = "CALL db.relationshipTypes()"
    relationship_types = gds.run_cypher(rel_types_query).values.flatten().tolist()
    
    return {
        'node_count': node_count,
        'node_labels': node_labels,
        'relationship_types': relationship_types
    }


def run_node_similarity(db_url: str, username: str, password: str, node_label: str, relationship_type: str, top_k: int = 10):
    gds = GraphDataScience(db_url, auth=(username, password), aura_ds=True)
    
    # Create a graph projection for node similarity
    graph_name = "node_sim_graph"
    
    # Project the graph
    projection_query = f"""
    CALL gds.graph.project(
        '{graph_name}',
        '{node_label}',
        '{relationship_type}'
    )
    """
    gds.run_cypher(projection_query)
    
    try:
        # Run node similarity
        similarity_query = f"""
        CALL gds.nodeSimilarity.stream('{graph_name}', {{
            topK: {top_k}
        }})
        YIELD node1, node2, similarity
        WITH gds.util.asNode(node1) as source,
             gds.util.asNode(node2) as target,
             similarity
        RETURN source.id as source_id,
               target.id as target_id,
               similarity
        ORDER BY similarity DESCENDING
        """
        
        result = gds.run_cypher(similarity_query)
        
        # Convert result to a list of dictionaries
        similarities = []
        for _, row in result.iterrows():
            similarities.append({
                'source_id': row['source_id'],
                'target_id': row['target_id'],
                'similarity': float(row['similarity'])
            })
            
        return similarities
        
    finally:
        # Clean up by dropping the projected graph
        cleanup_query = f"""
        CALL gds.graph.drop('{graph_name}')
        """
        gds.run_cypher(cleanup_query)

