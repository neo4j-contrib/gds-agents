from graphdatascience import GraphDataScience
import uuid
from contextlib import contextmanager
import logging
import os
import platform


def get_log_file_path():
    """Get the appropriate log file path based on the environment."""
    current_dir = os.getcwd()

    # Check if we're in development (project directory has pyproject.toml or src/)
    if os.path.exists(os.path.join(current_dir, "pyproject.toml")) or os.path.exists(
        os.path.join(current_dir, "src")
    ):
        return "mcp-server-neo4j-gds.log"

    # Production: use platform-specific Claude logs directory
    system = platform.system()
    home = os.path.expanduser("~")

    if system == "Darwin":  # macOS
        claude_logs_dir = os.path.join(home, "Library", "Logs", "Claude")
    elif system == "Windows":
        claude_logs_dir = os.path.join(
            os.environ.get("APPDATA", home), "Claude", "Logs"
        )
    else:  # Linux and other Unix-like systems
        claude_logs_dir = os.path.join(home, ".local", "share", "Claude", "logs")

    # Use Claude logs directory if it exists, otherwise fall back to current directory
    if os.path.exists(claude_logs_dir):
        return os.path.join(claude_logs_dir, "mcp-server-neo4j-gds.log")
    else:
        return "mcp-server-neo4j-gds.log"


log_file = get_log_file_path()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)
logger = logging.getLogger("mcp_server_neo4j_gds")


@contextmanager
def projected_graph(gds, undirected=False):
    """
    Project a graph from the database.

    Args:
        gds: GraphDataScience instance
        undirected: If True, project as undirected graph. Default is False (directed).
    """
    graph_name = f"temp_graph_{uuid.uuid4().hex[:8]}"
    try:
        rel_properties = gds.run_cypher(
            "MATCH (n)-[r]-(m) RETURN DISTINCT keys(properties(r))"
        )["keys(properties(r))"][0]
        # Include all properties that are not STRING
        valid_properties = {}
        for i in range(len(rel_properties)):
            pi = gds.run_cypher(
                f"MATCH (n)-[r]-(m) RETURN distinct r.{rel_properties[i]} IS :: STRING AS ISSTRING"
            )
            if pi.shape[0] == 1 and bool(pi["ISSTRING"][0]) is False:
                valid_properties[rel_properties[i]] = f"r.{rel_properties[i]}"
        prop_map = ", ".join(f"{prop}: r.{prop}" for prop in valid_properties)

        # Configure graph projection based on undirected parameter
        if undirected:
            # For undirected graphs, use undirectedRelationshipTypes: ['*'] to make all relationships undirected
            G, _ = gds.graph.cypher.project(
                f"""
                       MATCH (n)-[r]-(m)
                       WITH n, r, m
                       RETURN gds.graph.project(
                           $graph_name,
                           n,
                           m,
                           {{
                           sourceNodeLabels: labels(n),
                           targetNodeLabels: labels(m),
                           relationshipType: type(r),
                           relationshipProperties: {{{prop_map}}},
                           undirectedRelationshipTypes: ['*']
                       }}
                       )
                       """,
                graph_name=graph_name,
            )
        else:
            # Default directed projection
            G, _ = gds.graph.cypher.project(
                f"""
                       MATCH (n)-[r]-(m)
                       WITH n, r, m
                       RETURN gds.graph.project(
                           $graph_name,
                           n,
                           m,
                           {{
                           sourceNodeLabels: labels(n),
                           targetNodeLabels: labels(m),
                           relationshipType: type(r),
                           relationshipProperties: {{{prop_map}}}
                       }}
                       )
                       """,
                graph_name=graph_name,
            )
        yield G
    finally:
        gds.graph.drop(graph_name)


def count_nodes(gds: GraphDataScience):
    with projected_graph(gds) as G:
        return G.node_count()


def get_node_properties_keys(gds: GraphDataScience):
    with projected_graph(gds):
        query = """
        MATCH (n)
        RETURN DISTINCT keys(properties(n)) AS properties_keys
        """
        df = gds.run_cypher(query)
        if df.empty:
            return []
        return df["properties_keys"].iloc[0]
