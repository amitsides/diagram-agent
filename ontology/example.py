
# Example JSON representation
example_json = {
    "nodes": [
        {"id": "lb", "type": "ELB", "label": "lb"},
        {"id": "web", "type": "EC2", "label": "web"},
        {"id": "userdb", "type": "RDS", "label": "userdb"},
        {"id": "store", "type": "S3", "label": "store"},
        {"id": "stat", "type": "EC2", "label": "stat"}
    ],
    "edges": [
        {"source_id": "lb", "target_id": "web", "type": ">>", "properties": {}},
        {"source_id": "web", "target_id": "userdb", "type": ">>", "properties": {}},
        {"source_id": "userdb", "target_id": "store", "type": ">>", "properties": {}},
        {"source_id": "stat", "target_id": "userdb", "type": "<<", "properties": {}},
        {"source_id": "lb", "target_id": "web", "type": "-", "properties": {}}
    ]
}

# Example of how you might use this model to represent your diagram
def create_diagram_example():
    # Create nodes
    lb = Node(id="lb", type="ELB", label="lb")
    web = Node(id="web", type="EC2", label="web")
    userdb = Node(id="userdb", type="RDS", label="userdb")
    store = Node(id="store", type="S3", label="store")
    stat = Node(id="stat", type="EC2", label="stat")
    
    # Create edges
    edges = [
        Edge(source_id="lb", target_id="web", type=EdgeType.FORWARD),
        Edge(source_id="web", target_id="userdb", type=EdgeType.FORWARD),
        Edge(source_id="userdb", target_id="store", type=EdgeType.FORWARD),
        Edge(source_id="stat", target_id="userdb", type=EdgeType.BACKWARD),
        Edge(source_id="lb", target_id="web", type=EdgeType.BIDIRECTIONAL),
    ]
    
    # Create graph
    graph = Graph(nodes=[lb, web, userdb, store, stat], edges=edges)
    
    return graph