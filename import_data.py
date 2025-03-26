import os
from neo4j import GraphDatabase
import json

def import_tube_data(uri, username, password, data_file):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    # Load JSON data
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    with driver.session() as session:
        # Create constraints separately
        session.run("""
        CREATE CONSTRAINT underground_station_name IF NOT EXISTS FOR (s:UndergroundStation) REQUIRE s.name IS UNIQUE
        """)
        
        session.run("""
        CREATE CONSTRAINT underground_station_id IF NOT EXISTS FOR (s:UndergroundStation) REQUIRE s.id IS UNIQUE
        """)
        
        session.run("""
        UNWIND $stations AS station
        CREATE (s:UndergroundStation {
            id: station.id,
            name: station.name,
            display_name: CASE station.display_name 
                         WHEN 'NULL' THEN station.name 
                         ELSE station.display_name 
                         END,
            latitude: toFloat(station.latitude),
            longitude: toFloat(station.longitude),
            zone: CASE 
                  WHEN station.zone CONTAINS '.' THEN toFloat(station.zone)
                  ELSE toInteger(station.zone)
                  END,
            total_lines: toInteger(station.total_lines),
            rail: toInteger(station.rail)
        })
        """, {'stations': data['stations']})
        
        session.run("""
        UNWIND $connections AS conn
        MATCH (s1:UndergroundStation {id: conn.station1})
        MATCH (s2:UndergroundStation {id: conn.station2})
        CREATE (s1)-[r:LINK {
            line: conn.line,
            time: toInteger(conn.time),
            distance: toInteger(conn.time)
        }]->(s2)
        """, {'connections': data['connections']})
    
    driver.close()

# Usage
uri = os.environ["NEO4J_URI"]
username = os.environ["NEO4J_USERNAME"]
password = os.environ["NEO4J_PASSWORD"]
data_file = "dataset/london.json"

import_tube_data(uri, username, password, data_file)