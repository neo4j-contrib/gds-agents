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
        # Get relationship properties (non-string)
        rel_properties = get_relationship_properties_keys(gds)
        valid_rel_properties = {}
        for i in range(len(rel_properties)):
            pi = gds.run_cypher(
                f"MATCH (n)-[r]->(m) RETURN distinct r.{rel_properties[i]} IS :: STRING AS ISSTRING"
            )
            if pi.shape[0] == 1 and bool(pi["ISSTRING"][0]) is False:
                valid_rel_properties[rel_properties[i]] = f"r.{rel_properties[i]}"
        rel_prop_map = ", ".join(f"{prop}: r.{prop}" for prop in valid_rel_properties)

        # Get node properties (non-string, compatible with GDS)
        node_properties = get_node_properties_keys(gds)
        valid_node_properties_source = {}
        valid_node_properties_target = {}
        for i in range(len(node_properties)):
            # Check property types and whether all values are whole numbers
            type_check = gds.run_cypher(
                f"""
                MATCH (n) 
                WHERE n.{node_properties[i]} IS NOT NULL
                WITH n.{node_properties[i]} AS prop
                RETURN 
                    prop IS :: STRING AS IS_STRING,
                    prop IS :: LIST<FLOAT NOT NULL> AS IS_LIST_FLOAT,
                    prop IS :: LIST<INTEGER NOT NULL> AS IS_LIST_INTEGER,
                    CASE 
                        WHEN prop IS :: STRING THEN null
                        WHEN prop IS :: LIST<FLOAT NOT NULL> THEN null
                        WHEN prop IS :: LIST<INTEGER NOT NULL> THEN null
                        ELSE prop % 1 = 0 
                    END AS IS_WHOLE_NUMBER,
                    CASE 
                        WHEN prop IS :: STRING THEN null
                        WHEN prop IS :: LIST<FLOAT NOT NULL> THEN null
                        WHEN prop IS :: LIST<INTEGER NOT NULL> THEN null
                        ELSE prop % 1 <> 0 
                    END AS IS_DECIMAL
                LIMIT 10
                """
            )

            if not type_check.empty:
                # Check if any value is a string - if so, skip this property
                has_strings = any(type_check["IS_STRING"])
                if not has_strings:
                    all_numbers = (
                        type_check[["IS_WHOLE_NUMBER", "IS_DECIMAL"]]
                        .notna()
                        .any(axis=1)
                        .sum()
                        .item()
                    )
                    all_lists = (
                        type_check[["IS_LIST_FLOAT", "IS_LIST_INTEGER"]]
                        .any(axis=1)
                        .notna()
                        .sum()
                        .item()
                    )
                    if all_numbers == len(type_check):
                        # All values are numeric, check if all are whole numbers
                        whole_numbers = type_check["IS_WHOLE_NUMBER"].dropna()
                        if len(whole_numbers) > 0 and all(whole_numbers):
                            # All values are whole numbers - use as integer
                            valid_node_properties_source[node_properties[i]] = (
                                f"n.{node_properties[i]}"
                            )
                            valid_node_properties_target[node_properties[i]] = (
                                f"m.{node_properties[i]}"
                            )
                        else:
                            # Has decimal values - use as float
                            valid_node_properties_source[node_properties[i]] = (
                                f"toFloat(n.{node_properties[i]})"
                            )
                            valid_node_properties_target[node_properties[i]] = (
                                f"toFloat(m.{node_properties[i]})"
                            )
                    elif all_lists == len(type_check):
                        whole_numbers = type_check["IS_LIST_INTEGER"].dropna()
                        if len(whole_numbers) > 0 and all(whole_numbers):
                            # All values are  list of ints
                            valid_node_properties_source[node_properties[i]] = (
                                f"n.{node_properties[i]}"
                            )
                            valid_node_properties_target[node_properties[i]] = (
                                f"m.{node_properties[i]}"
                            )
                        else:
                            # Has at least an array of floats[]  - use as float list
                            valid_node_properties_source[node_properties[i]] = (
                                f"toFloatList(n.{node_properties[i]})"
                            )
                            valid_node_properties_target[node_properties[i]] = (
                                f"toFloatList(m.{node_properties[i]})"
                            )

        node_prop_map_source = ", ".join(
            f"{prop}: {expr}" for prop, expr in valid_node_properties_source.items()
        )

        node_prop_map_target = ", ".join(
            f"{prop}: {expr}" for prop, expr in valid_node_properties_target.items()
        )
        logger.info(f"Node property map source: '{node_prop_map_source}'")
        logger.info(f"Node property map target: '{node_prop_map_target}'")

        # Configure graph projection based on undirected parameter
        # Create data configuration (node/relationship structure)
        data_config_parts = [
            "sourceNodeLabels: labels(n)",
            "targetNodeLabels: labels(m)",
            "relationshipType: type(r)",
        ]

        if node_prop_map_source or node_prop_map_target:
            data_config_parts.extend(
                [
                    f"sourceNodeProperties: {{{node_prop_map_source}}}",
                    f"targetNodeProperties: {{{node_prop_map_target}}}",
                ]
            )

        if rel_prop_map:
            data_config_parts.append(f"relationshipProperties: {{{rel_prop_map}}}")

        data_config = ", ".join(data_config_parts)

        # Create additional configuration
        additional_config_parts = []
        if undirected:
            additional_config_parts.append("undirectedRelationshipTypes: ['*']")

        additional_config = (
            ", ".join(additional_config_parts) if additional_config_parts else ""
        )

        # Use separate data and additional configuration parameters
        if additional_config:
            project_query = f"""
                       MATCH (n)-[r]->(m)
                       WITH n, r, m
                       RETURN gds.graph.project(
                           $graph_name,
                           n,
                           m,
                           {{{data_config}}},
                           {{{additional_config}}}
                       )
                       """
            logger.info(f"Project query: '{project_query}'")
            G, _ = gds.graph.cypher.project(
                project_query,
                graph_name=graph_name,
            )
        else:
            projection_query = f"""
                       MATCH (n)-[r]->(m)
                       WITH n, r, m
                       RETURN gds.graph.project(
                           $graph_name,
                           n,
                           m,
                           {{{data_config}}}
                       )
                       """
            logger.info(f"Projection query: '{projection_query}'")
            G, _ = gds.graph.cypher.project(
                projection_query,
                graph_name=graph_name,
            )
        yield G
    finally:
        gds.graph.drop(graph_name)


def count_nodes(gds: GraphDataScience):
    with projected_graph(gds) as G:
        return G.node_count()


def get_node_properties_keys(gds: GraphDataScience):
    query = """
        MATCH (n)
        RETURN DISTINCT keys(properties(n)) AS properties_keys
        """
    df = gds.run_cypher(query)
    if df.empty:
        return []
    return df["properties_keys"].iloc[0]


def get_relationship_properties_keys(gds: GraphDataScience):
    query = """
        MATCH (n)-[r]->(m)
        RETURN DISTINCT keys(properties(r)) AS properties_keys
        """
    df = gds.run_cypher(query)
    if df.empty:
        return []
    return df["properties_keys"].iloc[0]
