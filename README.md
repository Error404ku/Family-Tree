# Interactive Family Tree System with Streamlit and Neo4j
![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-FF4B4B.svg)
![Neo4j](https://img.shields.io/badge/Neo4j-4.4.0-008CC1.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A web-based application for managing and visualizing family relationships using Streamlit for the frontend and Neo4j graph database for backend storage. Implements DFS and Greedy Best-First Search algorithms for family tree exploration.

## Features

- 🧑‍🤝‍🧑 **Family Relationship Management**
  - Add new family members
  - Create various relationships (parent, spouse, sibling, in-laws)
  - Delete individuals and their relationships
  - Auto-update of all relationships

- 🔍 **Advanced Search Capabilities**
  - Family tree visualization
  - Relationship discovery (ancestors, descendants, cousins, in-laws)
  - Two search algorithms:
    - Depth-First Search (DFS)
    - Greedy Best-First Search

- 📊 **Interactive Visualization**
  - Multiple display formats (text and table)
  - Search process visualization
  - Real-time family structure updates

## Installation

1. **Prerequisites**
   - Python 3.7+
   - Neo4j Database (version 4.4+)
   - pip package manager

2. **Clone Repository**
   ```bash
   git clone https://github.com/Error404ku/Family-Tree.git
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Neo4j Configuration**
   - Install and run Neo4j database
   - Update `config.py` with your Neo4j credentials:
     ```python
     NEO4J_URI = "bolt://localhost:7687"
     NEO4J_USER = "neo4j"
     NEO4J_PASSWORD = "your_password"
     ```

## Usage

1. **Start Application**
   ```bash
   streamlit run app.py
   ```

2. **Application Pages**
   - **Family Tree Search**: Explore family relationships using DFS or Greedy algorithms
   - **Add Individuals/Relations**: Manage family members and their connections
   - **Delete Individuals**: Remove family members from the system
   - **Update Relations**: Refresh all family relationships

3. **Search Features**
   - Select family member and search algorithm
   - Choose relationships to display (spouse, ancestors, descendants, etc.)
   - View search steps and process visualization

## Project Structure

```
family-tree-system/
├── app.py                 # Main Streamlit application
├── config.py              # Neo4j database configuration
├── dfs.py                 # DFS algorithm implementation
├── greedy_best_first.py   # Greedy Best-First Search implementation
├── neo4j_operation.py     # Neo4j database operations
└── requirements.txt       # Python dependencies
```

## Algorithms

1. **Depth-First Search (DFS)**
   - Implemented in `dfs.py`
   - Features:
     - Ancestor/descendant tracking
     - Path visualization
     - Multi-level relationship discovery

2. **Greedy Best-First Search**
   - Implemented in `greedy_best_first.py`
   - Features:
     - Heuristic-based search
     - Priority queue implementation
     - Search optimization for family relationships

## Configuration

Configure Neo4j connection in `config.py`:
```python
NEO4J_URI = "bolt://localhost:7687"  # Neo4j connection URI
NEO4J_USER = "neo4j"                 # Database username
NEO4J_PASSWORD = "secure_password"   # Database password
```

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Note:** Ensure Neo4j service is running before starting the application. The system will automatically create necessary nodes and relationships when first populated with data.
