import os

import pytest
from graphdatascience import GraphDataScience

from neo4j import GraphDatabase

NEO4J_IMAGE = "neo4j:2025.05.0"
NEO4J_BOLT_PORT = 7687
NEO4J_HTTP_PORT = 7474
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "testpassword"


@pytest.mark.asyncio
def test_node_projection_properties(neo4j_container):
    """Import test data into Neo4j."""
    # Set environment variables for the import script
    os.environ["NEO4J_URI"] = neo4j_container
    os.environ["NEO4J_USERNAME"] = NEO4J_USER
    os.environ["NEO4J_PASSWORD"] = NEO4J_PASSWORD

    driver = GraphDatabase.driver(neo4j_container, auth=(NEO4J_USER, NEO4J_PASSWORD))
    existing_count1 = -1
    existing_count2 = -2
    gds = GraphDataScience(driver)
    with driver.session() as session:
        session.run("CREATE (n:Foo {name:'a'})")
        session.run("CREATE (n:Foo {name:'b'})")

        session.run("MATCH (n)  WHERE n.name = 'a' SET n.propInt = 3")
        session.run("MATCH (n)  WHERE n.name = 'a' SET n.propDouble = 3.4")
        session.run("MATCH (n)  WHERE n.name = 'a' SET n.propListDouble = [3.4]")
        session.run("MATCH (n)  WHERE n.name = 'a' SET n.propListInt = [3]")
        session.run("MATCH (n)  WHERE n.name = 'a' SET n.propString = 'foo'")

        session.run("MATCH (n)  WHERE n.name = 'a' SET n.propIntDouble = 3.4")
        session.run("MATCH (n)  WHERE n.name = 'b' SET n.propIntDouble = 3")

        session.run("MATCH (n) WHERE n.name = 'a' SET  n.propListDoubleListInt = [3.4]")
        session.run("MATCH (n) WHERE n.name = 'b' SET  n.propListDoubleListInt = [3]")

        session.run(
            "MATCH (n) WHERE n.name = 'a' SET n.propListDoubleButInvalid = [3.4]"
        )
        session.run("MATCH (n)  WHERE n.name = 'b' SET n.propListDoubleButInvalid = 0")

        res = session.run("MATCH (n) WHERE 'Foo' IN labels(n) RETURN count(n) as count")
        existing_count1 = res.single()["count"]

    from mcp_server.src.mcp_server_neo4j_gds.gds import validate_properties

    projection_properties = validate_properties(
        gds,
        [
            "propInt",
            "propIntDouble",
            "propDouble",
            "propListDouble",
            "propListInt",
            "propString",
            "propListDoubleListInt",
            "propListDoubleButInvalid",
        ],
    )

    # remove data
    with driver.session() as session:
        session.run("MATCH (n)  REMOVE n.propInt")
        session.run("MATCH (n)  REMOVE n.propIntDouble")
        session.run("MATCH (n)  REMOVE n.propDouble")

        session.run("MATCH (n)  REMOVE n.propListDouble")
        session.run("MATCH (n)  REMOVE n.propListInt")
        session.run("MATCH (n)  REMOVE n.propString")

        session.run("MATCH (n)  REMOVE n.propListDoubleListInt")
        session.run("MATCH (n)  REMOVE n.propListDoubleButInvalid ")
        session.run("MATCH (n:Foo)  DETACH DELETE n")

        res = session.run("MATCH (n) WHERE 'Foo' IN labels(n) RETURN count(n) as count")
        existing_count2 = res.single()["count"]

    driver.close()

    assert "propString" not in projection_properties
    assert "propListDoubleButInvalid" not in projection_properties
    assert projection_properties["propInt"] == "INTEGER"
    assert projection_properties["propDouble"] == "FLOAT"
    assert projection_properties["propIntDouble"] == "FLOAT"
    assert projection_properties["propListDouble"] == "FLOAT_LIST"
    assert projection_properties["propListInt"] == "INTEGER_LIST"
    assert projection_properties["propListDoubleListInt"] == "FLOAT_LIST"
    assert existing_count1 == 2
    assert existing_count2 == 0
