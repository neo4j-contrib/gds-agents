# GDS Agent

Neither LLMs nor any existing toolings (MCP Servers) are capable of complex reasoning on graphs at the moment.

This MCP Server includes toolings from Neo4j Graph Data Science (GDS) library, which allows you to run all common graph algorithms.

Once the server is running, you are able to **ask any graph questions about your Neo4j graph** and get answers. LLMs equipped with GDS agent can decide and accurately execute the appropriate parameterised graph algorithms over the graph you have in your Neo4j database.

# Table of Contents

- [Setup](#setup)
- [Start the server](#start-the-server)
- [Example usage](#example-usage)
- [How to contribute](#how-to-contribute)
- [Feature request and bug reports](#feature-request-and-bug-reports)


# Setup
1. Install necessary packages in your python environment with `pip install -r requirements.txt`
2. Install the Neo4j database with GDS plugin:
   Download the Neo4j Desktop from [Neo4j Download Center](https://neo4j.com/download/)
   Install the GDS plugin from the Neo4j Desktop
   Create a new database and start it
3. Populate .env file with necessary credentials:
   ```bash
   NEO4J_URI=bolt://localhost:7687  # or other database URL if running in Aura
   NEO4J_USERNAME=neo4j  # or other customer name
   NEO4J_PASSWORD=your_password
   ```
4. Load the London Underground dataset with the following command:
   ```bash
   python import_data.py
   ```
Connect to your DB and querying the graph from [Neo4j workspace](https://workspace-preview.neo4j.io/workspace/), 
you should see:
![London Underground Graph](dataset/london-underground-graph.png)


# Start the server
Run `uv sync` and run `claude` from command line when inside the `mcp_server`.

# Example usage
An example usage where we can ask Claude (that have access to the gds-agent MCP server) questions regarding my graph.
It finds and executes the algorithms with appropriate parameters. Intermediate outputs are also shown.

```
> My database contains a graph about the London underground. I have some questions about my data. Use the available tools. If you cannot decide which tool to use, ask for confirmation.

⏺ I can help you analyze your London underground graph data! I have access to several Neo4j GDS tools for graph analysis including:

  - Node operations: Count nodes, get node properties
  - Centrality algorithms: PageRank, degree centrality, betweenness centrality, closeness centrality, eigenvector centrality, harmonic centrality, ArticleRank, HITS
  - Path algorithms: Find shortest paths between nodes
  - Graph structure: Find articulation points, bridges
  - Influence maximization: CELF algorithm

  What specific questions do you have about your London underground data? For example:
  - Which stations are most central/important?
  - What are the shortest paths between stations?
  - Which stations are critical connection points?
  - How many nodes/stations are in your graph?

  Let me know what you'd like to explore and I'll use the appropriate tools to analyze your data.

> How can I go from Embankment to Paddington quickly?

⏺ neo4j-gds:find_shortest_path (MCP)(start_node: "Embankment", end_node: "Paddington")…
  ⎿ {'totalCost': 6.0, 'nodeIds': [71, 251, 89, 25, 9, 68, 167], 'nodeNames': [<Node element_id='4:4da44164-1c21-4122-8b25-791a7359cb53:71' labels=frozenset({'UndergroundStation'}) properties={'zone': 1, 'latitude': 51.5074, 'rail': 0, 'name': 'Embankment', 'total_lines': 4, 'id': '87',
    'display_name': 'Embankment', 'longitude': -0.1223}>, <Node element_id='4:4da44164-1c21-4122-8b25-791a7359cb53:251' labels=frozenset({'UndergroundStation'}) properties={'zone': 1, 'latitude': 51.501, 'rail': 0, 'name': 'Westminster', 'total_lines': 3, 'id': '285', 'display_name': 'Westminster',
    'longitude': -0.1254}>, <Node element_id='4:4da44164-1c21-4122-8b25-791a7359cb53:89' labels=frozenset({'UndergroundStation'}) properties={'zone': 1, 'latitude': 51.5067, 'rail': 0, 'name': 'Green Park', 'total_lines': 3, 'id': '107', 'display_name': 'Green<br />Park', 'longitude': -0.1428}>, <Node
     element_id='4:4da44164-1c21-4122-8b25-791a7359cb53:25' labels=frozenset({'UndergroundStation'}) properties={'zone': 1, 'latitude': 51.5142, 'rail': 0, 'name': 'Bond Street', 'total_lines': 2, 'id': '28', 'display_name': 'Bond<br />Street', 'longitude': -0.1494}>, <Node
    element_id='4:4da44164-1c21-4122-8b25-791a7359cb53:9' labels=frozenset({'UndergroundStation'}) properties={'zone': 1, 'latitude': 51.5226, 'rail': 0, 'name': 'Baker Street', 'total_lines': 5, 'id': '11', 'display_name': 'Baker<br />Street', 'longitude': -0.1571}>, <Node
    element_id='4:4da44164-1c21-4122-8b25-791a7359cb53:68' labels=frozenset({'UndergroundStation'}) properties={'zone': 1, 'latitude': 51.5203, 'rail': 0, 'name': 'Edgware Road (C)', 'total_lines': 3, 'id': '83', 'display_name': 'Edgware<br />Road', 'longitude': -0.17}>, <Node
    element_id='4:4da44164-1c21-4122-8b25-791a7359cb53:167' labels=frozenset({'UndergroundStation'}) properties={'zone': 1, 'latitude': 51.5154, 'rail': 1, 'name': 'Paddington', 'total_lines': 4, 'id': '193', 'display_name': 'Paddington', 'longitude': -0.1755}>], 'path': <Path start=<Node
    element_id='4:4da44164-1c21-4122-8b25-791a7359cb53:71' labels=frozenset({'UndergroundStation'}) properties={'zone': 1, 'latitude': 51.5074, 'rail': 0, 'name': 'Embankment', 'total_lines': 4, 'id': '87', 'display_name': 'Embankment', 'longitude': -0.1223}> end=<Node
    element_id='4:4da44164-1c21-4122-8b25-791a7359cb53:167' labels=frozenset({'UndergroundStation'}) properties={'zone': 1, 'latitude': 51.5154, 'rail': 1, 'name': 'Paddington', 'total_lines': 4, 'id': '193', 'display_name': 'Paddington', 'longitude': -0.1755}> size=6>, 'costs': [0.0, 1.0, 2.0, 3.0,
    4.0, 5.0, 6.0]}

⏺ The quickest route from Embankment to Paddington takes 6 stops:

  Embankment → Westminster → Green Park → Bond Street → Baker Street → Edgware Road → Paddington

  Total cost: 6 stops

> How central is Piccadilly Circus in the London underground network?

⏺ neo4j-gds:degree_centrality (MCP)(nodes: ["Piccadilly Circus"])…

⏺ neo4j-gds:betweenness_centrality (MCP)(nodes: ["Piccadilly Circus"])…

⏺ neo4j-gds:closeness_centrality (MCP)(nodes: ["Piccadilly Circus"])…

⏺ neo4j-gds:pagerank (MCP)(nodes: ["Piccadilly Circus"])…

╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Tool use                                                                                                                                                                                                                                                                                                        │
│                                                                                                                                                                                                                                                                                                                 │
│   neo4j-gds:degree_centrality(nodes: ["Piccadilly Circus"]) (MCP)                                                                                                                                                                                                                                               │
│   Calculate degree centrality for all nodes in the graph                                                                                                                                                                                                                                                        │
│                                                                                                                                                                                                                                                                                                                 │
│ Do you want to proceed?                                                                                                                                                                                                                                                                                         │
│ ❯ 1. Yes                                                                                                                                                                                                                                                                                                        │
│   2. Yes, and don't ask again for neo4j-gds:degree_centrality commands in /Users/sbr/gds-agents/mcp_server                                                                                                                                                                                                      │
│   3. No, and tell Claude what to do differently (esc)                                                                                                                                                                                                                                                           │
│                                                                                                                                                                                                                                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

...

```

# How to contribute
Open a pull request from a branch of your forked repository into the main branch of this repo, for example `mygithubid:add-new-algo -> neo4j-contrib:main`.

The CI build in github action requires all codestyle checks and tests to pass.

To run and fix codestyle checks locally, in the `/mcp_server` directory, run:
```bash
uv sync --dev
```
to setup the python environment. And then,
```bash
uv run pytest tests -v -s
uv run ruff check
uv run ruff format
```
for all tests and codestyle fixes.

# Feature request and bug reports
To report a bug or a new feature request, raise an issue.
If it is a bug, include the full stacktrace and errors.
When available, attach relevant logs in `mcp_server_neo4j_gds.log` under your `src/mcp_server_neo4j_gds`, and relevant minimal dataset that can be used to reproduce the prboem.