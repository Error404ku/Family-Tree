import os
from neo4j import GraphDatabase  # Impor pustaka Neo4j untuk menghubungkan aplikasi dengan database Neo4j

# Ganti dengan kredensial Neo4j Anda
NEO4J_URI = "bolt://localhost:7687"  # Ganti dengan URI Neo4j Anda
NEO4J_USER = "neo4j"                  # Ganti dengan username Neo4j Anda
NEO4J_PASSWORD = "password"           # Ganti dengan password Neo4j Anda

# Buat instance driver Neo4j
# Driver ini digunakan untuk menghubungkan dan berinteraksi dengan database Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
