# gds-agents

# Setup
1. Install necessary packages in your python environment with `pip install -r requirements.txt`
2. Install the Neo4j database with GDS plugin:
   3. Download the Neo4j Desktop from [Neo4j Download Center](https://neo4j.com/download/)
   4. Install the GDS plugin from the Neo4j Desktop
   5. Create a new database and start it
3. Populate .env file with necessary credentials:
   ```bash
   NEO4J_URI=bolt://localhost:7687  # or other database URL if running in Aura
   NEO4J_USERNAME=neo4j  # or other customer name
   NEO4J_PASSWORD=your_password
   CLAUDE_API_KEY=your_api_key
   ```
4. Load the London Underground dataset with the following command:
   ```bash
   python import_data.py
   ```
Connect to your DB and querying the graph from [Neo4j workspace](https://workspace-preview.neo4j.io/workspace/), 
you should see:
![London Underground Graph](dataset/london-underground-graph.png)